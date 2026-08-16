from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Department, Role
from .serializers import DepartmentSerializer, RoleSerializer
from apps.employees.models import Employee
from attendance.models import Attendance
from payroll.models import SalaryStructure, PayrollRun
from django.utils import timezone
from django.db.models import Sum

from apps.common.permissions import IsAdminOrHRWriteElseReadOnly, IsExecutive

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrHRWriteElseReadOnly]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrHRWriteElseReadOnly]

class CEOMetricsView(APIView):
    permission_classes = [IsAuthenticated, IsExecutive]

    def get(self, request):
        today = timezone.now().date()

        # 1. Headcount
        total_employees = Employee.objects.filter(status='active').count()

        # 2. Today's Attendance
        present_today = Attendance.objects.filter(date=today, status__in=['PRESENT', 'LATE']).count()
        attendance_rate = (present_today / total_employees * 100) if total_employees > 0 else 0

        # 3. Monthly Payroll Estimate
        payroll_totals = SalaryStructure.objects.aggregate(
            basic=Sum("basic_salary"),
            housing=Sum("housing_allowance"),
            transport=Sum("transport_allowance"),
        )
        total_payroll = sum(value or 0 for value in payroll_totals.values())

        # 4. Department Breakdown
        departments = Department.objects.all()
        dept_breakdown = []
        for dept in departments:
            count = Employee.objects.filter(department=dept, status='active').count()
            if count > 0:
                dept_breakdown.append({
                    "name": dept.name,
                    "count": count
                })

        # 5. Recent Payroll Runs
        recent_runs = PayrollRun.objects.order_by('-month')[:3]
        recent_runs_data = [
            {
                "id": run.id,
                "month": run.month.strftime("%B %Y"),
                "is_finalized": run.is_finalized
            } for run in recent_runs
        ]

        return Response({
            "total_employees": total_employees,
            "attendance_rate": round(attendance_rate, 1),
            "total_monthly_payroll": total_payroll,
            "department_breakdown": dept_breakdown,
            "recent_payroll_runs": recent_runs_data
        })
