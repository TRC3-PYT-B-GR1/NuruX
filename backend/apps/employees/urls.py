from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, EmployeeMetricsView

router = DefaultRouter()
router.register("", EmployeeViewSet, basename="employee")

urlpatterns = [
    path('metrics/', EmployeeMetricsView.as_view(), name='employee-metrics'),
] + router.urls
