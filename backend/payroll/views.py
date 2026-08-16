from decimal import Decimal

from django.conf import settings
from django.db import transaction
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsPayrollAdminOrReadOnlyExecutive
from apps.employees.models import Employee
from .models import PayrollRun, Payslip, SalaryStructure
from .serializers import PayrollRunSerializer, PayslipSerializer, SalaryStructureSerializer


class SalaryStructureViewSet(viewsets.ModelViewSet):
    queryset = SalaryStructure.objects.select_related('employee__user').all()
    serializer_class = SalaryStructureSerializer
    permission_classes = [permissions.IsAuthenticated, IsPayrollAdminOrReadOnlyExecutive]


class PayrollRunViewSet(viewsets.ModelViewSet):
    queryset = PayrollRun.objects.select_related('processed_by').order_by('-month')
    serializer_class = PayrollRunSerializer
    permission_classes = [permissions.IsAuthenticated, IsPayrollAdminOrReadOnlyExecutive]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def perform_create(self, serializer):
        serializer.save(processed_by=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if self.get_object().is_finalized:
            return Response({'detail': 'A finalized payroll run is immutable.'}, status=409)
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def trigger_run(self, request, pk=None):
        run = PayrollRun.objects.select_for_update().get(pk=self.get_object().pk)
        if run.is_finalized:
            return Response({'detail': 'Payroll run is already finalized.'}, status=400)

        tax_rate = Decimal(settings.PAYROLL_TAX_RATE)
        pension_rate = Decimal(settings.PAYROLL_PENSION_RATE)
        nhf_rate = Decimal(settings.PAYROLL_NHF_RATE)
        employees = Employee.objects.filter(status=Employee.Status.ACTIVE).select_related(
            'salary_structure'
        )
        payslips_created = 0

        for employee in employees:
            try:
                structure = employee.salary_structure
            except SalaryStructure.DoesNotExist:
                continue

            basic = structure.basic_salary
            housing = structure.housing_allowance
            transport = structure.transport_allowance
            tax = basic * tax_rate
            pension = (
                structure.pension_override
                if structure.pension_override is not None
                else basic * pension_rate
            )
            nhf = basic * nhf_rate
            net = basic + housing + transport - tax - pension - nhf

            Payslip.objects.update_or_create(
                payroll_run=run,
                employee=employee,
                defaults={
                    'basic_salary': basic,
                    'housing_allowance': housing,
                    'transport_allowance': transport,
                    'tax_paye': tax,
                    'pension': pension,
                    'nhf': nhf,
                    'net_salary': net,
                },
            )
            payslips_created += 1

        run.is_finalized = True
        run.processed_by = request.user
        run.save(update_fields=['is_finalized', 'processed_by'])
        return Response({
            'detail': f'Generated {payslips_created} payslips.',
            'calculation_basis': 'Configured deployment rates',
        })


class PayslipViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PayslipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Payslip.objects.select_related('employee__user', 'payroll_run').order_by(
            '-payroll_run__month'
        )
        if user.is_superuser or user.role in {'super_admin', 'payroll_officer'}:
            return queryset
        profile = getattr(user, 'employee_profile', None)
        return queryset.filter(employee=profile) if profile else queryset.none()
