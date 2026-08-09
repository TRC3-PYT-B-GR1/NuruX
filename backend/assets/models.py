
from django.db import models


class EmployeeAsset(models.Model):
    ASSET_TYPES = [
        ('Laptop', 'Laptop'),
        ('Phone', 'Phone'),
        ('ID Card', 'ID Card'),
        ('Other', 'Other'),
    ]

    asset_name = models.CharField(max_length=100)

    asset_type = models.CharField(
        max_length=50,
        choices=ASSET_TYPES
    )

    serial_number = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.asset_name
    
class AssetAssignment(models.Model):
    asset = models.ForeignKey(
        EmployeeAsset,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    employee_name = models.CharField(max_length=100)

    assigned_date = models.DateField()

    status_choices = [
        ('Assigned', 'Assigned'),
        ('Returned', 'Returned'),
    ]

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default='Assigned'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset} assigned to {self.employee_name}"
    
class AssetReturn(models.Model):
    assignment = models.ForeignKey(
        AssetAssignment,
        on_delete=models.CASCADE,
        related_name='returns'
    )

    return_date = models.DateField()

    condition = models.CharField(
        max_length=100
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Return of {self.assignment.asset}"
    
class MaintenanceHistory(models.Model):
    asset = models.ForeignKey(
        EmployeeAsset,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )

    maintenance_date = models.DateField()

    description = models.TextField()

    status_choices = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.asset} maintenance"