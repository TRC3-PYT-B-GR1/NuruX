from django.contrib import admin
from .models import (
    EmployeeAsset,
    AssetAssignment,
    AssetReturn,
    MaintenanceHistory
)


admin.site.register(EmployeeAsset)
admin.site.register(AssetAssignment)
admin.site.register(AssetReturn)
admin.site.register(MaintenanceHistory)

# Register your models here.
