from django.db import models
from apps.employees.models import Employee
from django.conf import settings

class SalaryStructure(models.Model):
    employee = models.OneToOneField(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='salary_structure'
    )
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    housing_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # These are usually percentages, but storing actual expected values or overrides might be useful
    # For now we assume statutory rates are computed dynamically unless overridden here
    pension_override = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Salary Structure for {self.employee}"

class PayrollRun(models.Model):
    month = models.DateField(help_text="The month and year for this payroll run (usually first day of month)")
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_finalized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payroll Run - {self.month.strftime('%B %Y')}"

class Payslip(models.Model):
    payroll_run = models.ForeignKey(
        PayrollRun,
        on_delete=models.CASCADE,
        related_name='payslips'
    )
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='payslips'
    )
    
    # Earnings
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    housing_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    bonuses = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Deductions
    tax_paye = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pension = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    nhf = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    loan_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    leave_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Net
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('payroll_run', 'employee')
        
    def __str__(self):
        return f"Payslip - {self.employee} - {self.payroll_run.month.strftime('%B %Y')}"
