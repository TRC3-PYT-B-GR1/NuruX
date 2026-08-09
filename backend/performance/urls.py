from django.urls import path
from .views import KPIListCreateAPIView, GoalListCreateAPIView, PerformanceReviewListCreateAPIView, ManagerFeedbackListCreateAPIView


urlpatterns = [
    path('kpis/', KPIListCreateAPIView.as_view(), name='kpis-list'),
    path('goals/', GoalListCreateAPIView.as_view(), name='goals-list'),
    path('reviews/', PerformanceReviewListCreateAPIView.as_view(), name='reviews-list'),
    path('feedback/',ManagerFeedbackListCreateAPIView.as_view(), name='feedback-list'),
]