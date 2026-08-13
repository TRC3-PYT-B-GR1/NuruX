from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveBalanceViewSet, LeaveRequestViewSet

router = DefaultRouter()
router.register(r'leave-balances', LeaveBalanceViewSet, basename='leave-balance')
router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')

urlpatterns = [
    path('', include(router.urls)),
]
