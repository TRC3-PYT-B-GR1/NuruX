from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Department
from .serializers import CustomTokenObtainPairSerializer, DepartmentSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for Departments. 
    Only authenticated users can view, only HR or Admin can modify.
    For simplicity in Phase 1, using IsAdminUser or custom permissions later.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Assuming is_staff = True for Admins/HR
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()
