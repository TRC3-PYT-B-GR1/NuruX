from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Count
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAdminOrHR, IsManagerOrHR
from apps.organizations.models import Department
from attendance.models import Attendance
from .models import Certification, EducationRecord, Employee, EmployeeSkill, EmploymentHistory, PromotionHistory
from .serializers import (
    CertificationApiSerializer, EducationRecordApiSerializer, EmployeeCreateSerializer,
    EmployeeSerializer, EmployeeSkillApiSerializer, EmploymentHistoryApiSerializer,
    PromotionHistoryApiSerializer,
)

User = get_user_model()


class EmployeeViewSet(viewsets.ModelViewSet):
    """Role-scoped employee directory with HR-only mutations."""

    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_permissions(self):
        if self.action in {'create', 'partial_update'}:
            return [permissions.IsAuthenticated(), IsAdminOrHR()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        queryset = Employee.objects.select_related('department', 'role', 'user', 'manager').prefetch_related(
            'employment_history', 'education_records', 'certifications', 'skills', 'promotion_history'
        )
        if user.is_superuser or user.role in {'super_admin', 'hr_officer', 'director'}:
            return queryset.all()
        if user.role == 'manager':
            employee = getattr(user, 'employee_profile', None)
            if employee and employee.department_id:
                return queryset.filter(department_id=employee.department_id)
            return queryset.none()
        employee = getattr(user, 'employee_profile', None)
        return queryset.filter(pk=employee.pk) if employee else queryset.none()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        input_serializer = EmployeeCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        requested_role = data['rbac_role']
        if requested_role == User.Role.SUPER_ADMIN and not (
            request.user.is_superuser or request.user.role == User.Role.SUPER_ADMIN
        ):
            return Response(
                {'rbac_role': ['Only a super administrator can create another super administrator.']},
                status=status.HTTP_403_FORBIDDEN,
            )

        base_username = slugify(data['email'].split('@', 1)[0])[:140] or 'employee'
        username = base_username
        suffix = 1
        while User.objects.filter(username=username).exists():
            suffix += 1
            username = f'{base_username}{suffix}'

        user = User.objects.create_user(
            username=username,
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=requested_role,
        )
        employee = Employee.objects.create(
            user=user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            department=data['department'],
            role=data['role'],
            date_joined=timezone.localdate(),
            status=Employee.Status.ACTIVE,
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender', ''),
            nationality=data.get('nationality', ''),
            identification_number=data.get('identification_number', ''),
            employment_type=data.get('employment_type', Employee.EmploymentType.FULL_TIME),
            salary_grade=data.get('salary_grade', ''),
            manager=data.get('manager'),
            emergency_contact_name=data.get('emergency_contact_name', ''),
            emergency_contact_relationship=data.get('emergency_contact_relationship', ''),
            emergency_contact_phone=data.get('emergency_contact_phone', ''),
            emergency_contact_address=data.get('emergency_contact_address', ''),
            next_of_kin_name=data.get('next_of_kin_name', ''),
            next_of_kin_relationship=data.get('next_of_kin_relationship', ''),
            next_of_kin_phone=data.get('next_of_kin_phone', ''),
            next_of_kin_address=data.get('next_of_kin_address', ''),
        )

        transaction.on_commit(
            lambda: send_mail(
                subject='Welcome to NuruX',
                message=(
                    f"Hello {employee.first_name},\n\n"
                    f"Your NuruX username is {username}.\n"
                    f"Your temporary password is: {data['password']}\n\n"
                    "Please log in and change your password immediately."
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
        )
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)


class EmployeeMetricsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManagerOrHR]

    def get(self, request):
        user = request.user
        today = timezone.localdate()

        if user.is_superuser or user.role in {'super_admin', 'hr_officer', 'director'}:
            employee_qs = Employee.objects.filter(status=Employee.Status.ACTIVE)
            department_qs = Department.objects.all()
            attendance_qs = Attendance.objects.filter(date=today)
        else:
            profile = getattr(user, 'employee_profile', None)
            if not profile or not profile.department_id:
                return Response({'detail': 'Manager has no assigned department.'}, status=400)
            employee_qs = Employee.objects.filter(
                status=Employee.Status.ACTIVE,
                department_id=profile.department_id,
            )
            department_qs = Department.objects.filter(id=profile.department_id)
            attendance_qs = Attendance.objects.filter(
                date=today,
                employee__department_id=profile.department_id,
            )

        headcounts = employee_qs.values('department__name').annotate(count=Count('id'))
        clock_ins = attendance_qs.filter(clock_in__isnull=False)
        clock_outs = attendance_qs.filter(clock_out__isnull=False)

        return Response({
            'total_headcount': employee_qs.count(),
            'total_departments': department_qs.count(),
            'headcount_by_department': [
                {'name': item['department__name'], 'count': item['count']}
                for item in headcounts if item['department__name']
            ],
            'total_clock_ins': clock_ins.count(),
            'clock_ins_by_department': [
                {'name': item['employee__department__name'], 'count': item['count']}
                for item in clock_ins.values('employee__department__name').annotate(count=Count('id'))
                if item['employee__department__name']
            ],
            'total_clock_outs': clock_outs.count(),
            'clock_outs_by_department': [
                {'name': item['employee__department__name'], 'count': item['count']}
                for item in clock_outs.values('employee__department__name').annotate(count=Count('id'))
                if item['employee__department__name']
            ],
        })


class EmployeeRecordViewSet(viewsets.ModelViewSet):
    """CRUD for profile history records, scoped to the employee's permissions."""
    permission_classes = [permissions.IsAuthenticated]
    model = None
    serializer_class = None

    def get_permissions(self):
        if self.action in {'create', 'update', 'partial_update', 'destroy'}:
            return [permissions.IsAuthenticated(), IsAdminOrHR()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = self.model.objects.select_related('employee')
        user = self.request.user
        if user.is_superuser or user.role in {'super_admin', 'hr_officer', 'director'}:
            return queryset
        profile = getattr(user, 'employee_profile', None)
        if user.role == 'manager' and profile and profile.department_id:
            return queryset.filter(employee__department_id=profile.department_id)
        return queryset.filter(employee=profile) if profile else queryset.none()


class EmploymentHistoryViewSet(EmployeeRecordViewSet):
    model = EmploymentHistory
    serializer_class = EmploymentHistoryApiSerializer


class EducationRecordViewSet(EmployeeRecordViewSet):
    model = EducationRecord
    serializer_class = EducationRecordApiSerializer


class CertificationViewSet(EmployeeRecordViewSet):
    model = Certification
    serializer_class = CertificationApiSerializer


class EmployeeSkillViewSet(EmployeeRecordViewSet):
    model = EmployeeSkill
    serializer_class = EmployeeSkillApiSerializer


class PromotionHistoryViewSet(EmployeeRecordViewSet):
    model = PromotionHistory
    serializer_class = PromotionHistoryApiSerializer
