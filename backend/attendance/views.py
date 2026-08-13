import math
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer, ClockInSerializer, ClockOutSerializer

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

class AttendanceViewSet(viewsets.ModelViewSet):
    """
    CRUD for Attendance.
    Employees can view their own and clock in/out.
    HR/Admins can view/edit all.
    """
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Attendance.objects.all()
        if hasattr(user, 'employee_profile'):
            return Attendance.objects.filter(employee=user.employee_profile)
        return Attendance.objects.none()

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def clock_in(self, request):
        serializer = ClockInSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employee = request.user.employee_profile
        except:
            return Response({"detail": "User has no employee profile."}, status=status.HTTP_400_BAD_REQUEST)
        
        today = timezone.now().date()
        
        gps_in = serializer.validated_data['gps_location']
        is_anomaly = False
        anomaly_reason = ""
        
        # Check against department location
        if employee.department and employee.department.latitude and employee.department.longitude:
            try:
                lat1, lon1 = map(float, gps_in.split(','))
                lat2, lon2 = float(employee.department.latitude), float(employee.department.longitude)
                dist_km = haversine(lat1, lon1, lat2, lon2)
                if dist_km > 0.2: # 200 meters threshold
                    is_anomaly = True
                    anomaly_reason = f"GPS LOCATION MISMATCH: Detected {dist_km:.2f} km away from office."
            except Exception as e:
                is_anomaly = True
                anomaly_reason = "GPS LOCATION ERROR: Could not parse or calculate location."

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={
                'clock_in': timezone.now(),
                'gps_location_in': gps_in,
                'status': Attendance.Status.PRESENT,
                'is_anomaly': is_anomaly,
                'anomaly_reason': anomaly_reason
            }
        )
        
        if not created and attendance.clock_in:
            return Response({"detail": "Already clocked in today."}, status=status.HTTP_400_BAD_REQUEST)
            
        if not created:
            attendance.clock_in = timezone.now()
            attendance.gps_location_in = gps_in
            attendance.status = Attendance.Status.PRESENT
            attendance.is_anomaly = is_anomaly
            attendance.anomaly_reason = anomaly_reason
            attendance.save()

        return Response(AttendanceSerializer(attendance).data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def clock_out(self, request):
        serializer = ClockOutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employee = request.user.employee_profile
        except:
            return Response({"detail": "User has no employee profile."}, status=status.HTTP_400_BAD_REQUEST)
            
        today = timezone.now().date()
        try:
            attendance = Attendance.objects.get(employee=employee, date=today)
        except Attendance.DoesNotExist:
            return Response({"detail": "No clock in record found for today."}, status=status.HTTP_400_BAD_REQUEST)
            
        if attendance.clock_out:
            return Response({"detail": "Already clocked out today."}, status=status.HTTP_400_BAD_REQUEST)
            
        attendance.clock_out = timezone.now()
        attendance.gps_location_out = serializer.validated_data['gps_location']
        attendance.save()
        
        return Response(AttendanceSerializer(attendance).data)
