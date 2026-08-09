from django.shortcuts import render
from rest_framework import generics
from .models import KPI, Goal, ManagerFeedback, PerformanceReview
from .serializers import GoalSerializer, KPISerializer, ManagerFeedbackSerializer, PerformanceReviewSerializer

# Create your views here.

class KPIListCreateAPIView(generics.ListCreateAPIView):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer
    
class GoalListCreateAPIView(generics.ListCreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class PerformanceReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    
class ManagerFeedbackListCreateAPIView(generics.ListCreateAPIView):
    queryset = ManagerFeedback.objects.all()
    serializer_class = ManagerFeedbackSerializer