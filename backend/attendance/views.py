import math
from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from .models import Attendance
from .serializers import AttendanceSerializer, ClockInSerializer, ClockOutSerializer


def haversine(lat1, lon1, lat2, lon2):
    """Return the great-circle distance between two coordinates in kilometres."""

    radius_km = 6371.0
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(delta_lon / 2) ** 2
    )
    return radius_km * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def parse_qr_token(token_string, employee):
    try:
        token = AccessToken(token_string)
    except TokenError as exc:
        raise ValueError('QR token is invalid or has expired.') from exc

    if token.get('type') != 'attendance_qr':
        raise ValueError('Invalid QR token type.')

    token_department = token.get('department_id')
    if token_department != 'all' and str(employee.department_id) != str(token_department):
        raise ValueError('QR token does not belong to your department.')
    return token


def evaluate_geofence(employee, gps_location):
    department = employee.department
    if not department or department.latitude is None or department.longitude is None:
        return False, ''

    latitude, longitude = (float(value) for value in gps_location.split(','))
    distance_km = haversine(
        latitude,
        longitude,
        float(department.latitude),
        float(department.longitude),
    )
    allowed_km = department.geofence_radius_meters / 1000
    if distance_km > allowed_km:
        return True, (
            f'GPS location mismatch: detected {distance_km:.2f} km from the office '
            f'(allowed {department.geofence_radius_meters} m).'
        )
    return False, ''


def attendance_status(now):
    workday_start = datetime.strptime(settings.WORKDAY_START, '%H:%M').time()
    threshold = datetime.combine(now.date(), workday_start) + timedelta(
        minutes=settings.ATTENDANCE_GRACE_MINUTES
    )
    return Attendance.Status.LATE if now.replace(tzinfo=None) > threshold else Attendance.Status.PRESENT


def overtime_hours(now):
    workday_end = datetime.strptime(settings.WORKDAY_END, '%H:%M').time()
    end = timezone.make_aware(datetime.combine(timezone.localdate(now), workday_end))
    seconds = max(0, (now - end).total_seconds())
    return Decimal(str(round(seconds / 3600, 2)))


class AttendanceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Immutable attendance history plus dedicated clock-in/out actions."""

    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Attendance.objects.select_related(
            'employee__department', 'employee__role', 'employee__user', 'shift'
        ).order_by('-date', '-clock_in')
        if user.is_superuser or user.role in {'super_admin', 'hr_officer', 'director'}:
            return queryset
        profile = getattr(user, 'employee_profile', None)
        if user.role == 'manager' and profile and profile.department_id:
            return queryset.filter(employee__department_id=profile.department_id)
        return queryset.filter(employee=profile) if profile else queryset.none()

    def _employee(self, request):
        employee = getattr(request.user, 'employee_profile', None)
        if not employee:
            return None, Response(
                {'detail': 'User has no employee profile.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if employee.status != employee.Status.ACTIVE:
            return None, Response(
                {'detail': 'Only active employees can record attendance.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return employee, None

    @action(detail=False, methods=['get'])
    def generate_qr(self, request):
        allowed_roles = {'manager', 'hr_officer', 'super_admin', 'director', 'receptionist'}
        if not (request.user.is_superuser or request.user.role in allowed_roles):
            return Response({'detail': 'Not authorized to generate QR.'}, status=403)

        token = AccessToken()
        token.set_exp(lifetime=timedelta(minutes=1))
        token['type'] = 'attendance_qr'
        profile = getattr(request.user, 'employee_profile', None)
        token['department_id'] = (
            profile.department_id
            if request.user.role == 'manager' and profile and profile.department_id
            else 'all'
        )
        token['issued_by'] = request.user.pk
        return Response({'qr_token': str(token), 'expires_in_seconds': 60})

    @action(detail=False, methods=['get'])
    def today(self, request):
        employee, error = self._employee(request)
        if error:
            return error
        record = self.get_queryset().filter(employee=employee, date=timezone.localdate()).first()
        return Response({
            'attendance': AttendanceSerializer(record).data if record else None,
            'is_checked_in': bool(record and record.clock_in and not record.clock_out),
            'is_checked_out': bool(record and record.clock_out),
        })

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def clock_in(self, request):
        serializer = ClockInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee, error = self._employee(request)
        if error:
            return error

        try:
            parse_qr_token(serializer.validated_data['qr_token'], employee)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        today = timezone.localdate()
        now = timezone.now()
        now_local = timezone.localtime(now)
        gps_location = serializer.validated_data['gps_location']
        is_anomaly, anomaly_reason = evaluate_geofence(employee, gps_location)

        attendance, created = Attendance.objects.select_for_update().get_or_create(
            employee=employee,
            date=today,
            defaults={
                'clock_in': now,
                'gps_location_in': gps_location,
                'status': attendance_status(now_local),
                'is_anomaly': is_anomaly,
                'anomaly_reason': anomaly_reason,
            },
        )
        if not created and attendance.clock_in:
            return Response({'detail': 'Already clocked in today.'}, status=400)
        if not created:
            attendance.clock_in = now
            attendance.gps_location_in = gps_location
            attendance.status = attendance_status(now_local)
            attendance.is_anomaly = is_anomaly
            attendance.anomaly_reason = anomaly_reason
            attendance.save()

        return Response(
            AttendanceSerializer(attendance).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def clock_out(self, request):
        serializer = ClockOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee, error = self._employee(request)
        if error:
            return error

        try:
            parse_qr_token(serializer.validated_data['qr_token'], employee)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            attendance = Attendance.objects.select_for_update().get(
                employee=employee,
                date=timezone.localdate(),
            )
        except Attendance.DoesNotExist:
            return Response({'detail': 'No clock-in record found for today.'}, status=400)
        if attendance.clock_out:
            return Response({'detail': 'Already clocked out today.'}, status=400)

        now = timezone.now()
        gps_location = serializer.validated_data['gps_location']
        is_anomaly, anomaly_reason = evaluate_geofence(employee, gps_location)
        attendance.clock_out = now
        attendance.gps_location_out = gps_location
        attendance.overtime_hours = overtime_hours(now)
        if is_anomaly:
            attendance.is_anomaly = True
            attendance.anomaly_reason = '; '.join(
                reason for reason in [attendance.anomaly_reason, anomaly_reason] if reason
            )
        attendance.save()
        return Response(AttendanceSerializer(attendance).data)
