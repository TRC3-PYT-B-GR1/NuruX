# from rest_framework.routers import DefaultRouter

# from .views import DepartmentViewSet, RoleViewSet

# router = DefaultRouter()
# router.register("departments", DepartmentViewSet, basename="department")
# router.register("roles", RoleViewSet, basename="role")

# urlpatterns = router.urls
from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet, RoleViewSet, CEOMetricsView
from django.urls import path


router = DefaultRouter()

router.register("departments", DepartmentViewSet, basename="department")
router.register("roles", RoleViewSet, basename="role")

urlpatterns = [
    path('ceo-metrics/', CEOMetricsView.as_view(), name='ceo-metrics'),
] + router.urls