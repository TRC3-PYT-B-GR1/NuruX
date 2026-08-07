from rest_framework import generics
from .models import Course, Assessment, Certificate
from .serializers import CourseSerializer, AssessmentSerializer, CertificateSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AssessmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    
class CertificateListCreateAPIView(generics.ListCreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer