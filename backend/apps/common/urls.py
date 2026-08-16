from django.urls import path
from .views import HealthView, LatestAppVersionView

urlpatterns = [
    path('health/', HealthView.as_view(), name='health'),
    path('system/latest-version/', LatestAppVersionView.as_view(), name='latest_version'),
]

from .views import AIChatView, AIInsightsView

urlpatterns.extend([
    path('ai/query/', AIChatView.as_view(), name='ai_query'),
    path('ai/insights/', AIInsightsView.as_view(), name='ai_insights'),
])

