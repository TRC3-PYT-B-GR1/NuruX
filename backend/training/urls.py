from django.urls import path

from training.models import Certificate
from .views import (
    CertificateListCreateAPIView,
    CertificateListCreateAPIView,
    CourseListCreateAPIView,
    AssessmentListCreateAPIView
)


urlpatterns = [
    path('courses/', CourseListCreateAPIView.as_view(), name='courses-list'),
    path('assessments/', AssessmentListCreateAPIView.as_view(), name='assessments-list'),
    path('certificates/', CertificateListCreateAPIView.as_view(), name='certificates-list'),
]