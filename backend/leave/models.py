from django.db import models
from apps.employees.models import Employee
from django.conf import settings

class LeaveType(models.TextChoices):
    ANNUAL = 'ANNUAL', 'Annual Leave'
    CASUAL = 'CASUAL', 'Casual Leave'
    STUDY = 'STUDY', 'Study Leave'
    COMPASSIONATE = 'COMPASSIONATE', 'Compassionate Leave'
    MATERNITY = 'MATERNITY', 'Maternity Leave'
    PATERNITY = 'PATERNITY', 'Paternity Leave'
    MEDICAL = 'MEDICAL', 'Medical Leave'

class LeaveBalance(models.Model):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )
    leave_type = models.CharField(
        max_length=20,
        choices=LeaveType.choices
    )
    year = models.IntegerField()
    total_allocated = models.IntegerField(default=0)
    used_days = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('employee', 'leave_type', 'year')
        
    def __str__(self):
        return f"{self.employee} - {self.get_leave_type_display()} ({self.year})"
    
    @property
    def remaining_days(self):
        return self.total_allocated - self.used_days

class LeaveRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED_BY_MANAGER = 'APPROVED_BY_MANAGER', 'Approved by Manager'
        APPROVED_BY_HR = 'APPROVED_BY_HR', 'Approved by HR'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'

    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.CharField(
        max_length=20,
        choices=LeaveType.choices
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    manager_approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manager_leave_approvals'
    )
    hr_approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hr_leave_approvals'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.get_leave_type_display()} ({self.start_date} to {self.end_date})"
