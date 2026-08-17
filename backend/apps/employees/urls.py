from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CertificationViewSet, EducationRecordViewSet, EmployeeMetricsView,
    EmployeeSkillViewSet, EmployeeViewSet, EmploymentHistoryViewSet,
    PromotionHistoryViewSet,
)

router = DefaultRouter()
router.register("employment-history", EmploymentHistoryViewSet, basename="employment-history")
router.register("education", EducationRecordViewSet, basename="education")
router.register("certifications", CertificationViewSet, basename="certification")
router.register("skills", EmployeeSkillViewSet, basename="employee-skill")
router.register("promotions", PromotionHistoryViewSet, basename="promotion-history")
router.register("", EmployeeViewSet, basename="employee")

urlpatterns = [
    path('metrics/', EmployeeMetricsView.as_view(), name='employee-metrics'),
] + router.urls
