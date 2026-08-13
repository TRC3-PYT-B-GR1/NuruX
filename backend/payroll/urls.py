from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalaryStructureViewSet, PayrollRunViewSet, PayslipViewSet

router = DefaultRouter()
router.register(r'salary-structures', SalaryStructureViewSet, basename='salary-structure')
router.register(r'payroll-runs', PayrollRunViewSet, basename='payroll-run')
router.register(r'payslips', PayslipViewSet, basename='payslip')

urlpatterns = [
    path('', include(router.urls)),
]
