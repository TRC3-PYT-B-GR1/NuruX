from django.db import models
from employees.models import Employee

class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        LATE = 'LATE', 'Late'
        HALF_DAY = 'HALF_DAY', 'Half-Day'
        REMOTE = 'REMOTE', 'Remote Work'

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date = models.DateField()
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABSENT
    )
    
    gps_location_in = models.CharField(max_length=255, blank=True, null=True, help_text="Lat/Long coordinate on clock-in")
    gps_location_out = models.CharField(max_length=255, blank=True, null=True, help_text="Lat/Long coordinate on clock-out")
    
    is_anomaly = models.BooleanField(default=False, help_text="Flagged if gps mismatch or other issue")
    anomaly_reason = models.TextField(blank=True, null=True)

    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee} - {self.date} ({self.get_status_display()})"
