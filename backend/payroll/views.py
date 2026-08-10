from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SalaryStructure, PayrollRun, Payslip
from apps.employees.models import Employee
from .serializers import SalaryStructureSerializer, PayrollRunSerializer, PayslipSerializer
from decimal import Decimal

class SalaryStructureViewSet(viewsets.ModelViewSet):
    queryset = SalaryStructure.objects.all()
    serializer_class = SalaryStructureSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class PayrollRunViewSet(viewsets.ModelViewSet):
    queryset = PayrollRun.objects.all()
    serializer_class = PayrollRunSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(processed_by=self.request.user)

    @action(detail=True, methods=['post'])
    def trigger_run(self, request, pk=None):
        """
        Calculates and generates payslips for all active employees for this payroll run.
        """
        run = self.get_object()
        if run.is_finalized:
            return Response({"detail": "Payroll run is already finalized."}, status=status.HTTP_400_BAD_REQUEST)
        
        employees = Employee.objects.all() # In reality, filter by active status
        payslips_created = 0
        
        for employee in employees:
            try:
                struct = employee.salary_structure
            except SalaryStructure.DoesNotExist:
                continue
                
            # Basic calculation for Phase 1
            basic = struct.basic_salary
            housing = struct.housing_allowance
            transport = struct.transport_allowance
            
            # Statutory (dummy percentages for demo)
            tax = basic * Decimal('0.05')
            pension = basic * Decimal('0.08')
            nhf = basic * Decimal('0.025')
            
            net = (basic + housing + transport) - (tax + pension + nhf)
            
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
                    'net_salary': net
                }
            )
            payslips_created += 1
            
        run.is_finalized = True
        run.save()
        
        return Response({"detail": f"Generated {payslips_created} payslips successfully."})

class PayslipViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PayslipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payslip.objects.all()
        if hasattr(user, 'employee_profile'):
            return Payslip.objects.filter(employee=user.employee_profile)
        return Payslip.objects.none()
