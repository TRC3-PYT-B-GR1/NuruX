from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    CRUD for Employee records.
    HR and Admins can do everything.
    Standard employees can only fetch their own profile via the /me/ endpoint.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Only Admins/HR can modify or list all employees
        if self.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Returns the Employee profile for the currently logged in user.
        """
        try:
            employee = request.user.employee_profile
            serializer = self.get_serializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "No employee profile found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )
