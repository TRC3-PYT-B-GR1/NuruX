from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsAdminOrHR, IsAdminOrHRWriteElseReadOnly
from .models import Course, Assessment, Certificate
from .serializers import CourseSerializer, AssessmentSerializer, CertificateSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrHRWriteElseReadOnly]


class AssessmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrHRWriteElseReadOnly]
    
class CertificateListCreateAPIView(generics.ListCreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrHR]
