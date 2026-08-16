from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsManagerOrHR
from .models import KPI, Goal, ManagerFeedback, PerformanceReview
from .serializers import GoalSerializer, KPISerializer, ManagerFeedbackSerializer, PerformanceReviewSerializer

# Create your views here.

class KPIListCreateAPIView(generics.ListCreateAPIView):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer
    permission_classes = [IsAuthenticated, IsManagerOrHR]
    
class GoalListCreateAPIView(generics.ListCreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, IsManagerOrHR]

class PerformanceReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated, IsManagerOrHR]
    
class ManagerFeedbackListCreateAPIView(generics.ListCreateAPIView):
    queryset = ManagerFeedback.objects.all()
    serializer_class = ManagerFeedbackSerializer
    permission_classes = [IsAuthenticated, IsManagerOrHR]
