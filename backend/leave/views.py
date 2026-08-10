from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LeaveBalance, LeaveRequest
from .serializers import LeaveBalanceSerializer, LeaveRequestSerializer, LeaveApproveSerializer

class LeaveBalanceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Employees can view their own balances.
    HR/Admin can view all.
    """
    serializer_class = LeaveBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LeaveBalance.objects.all()
        if hasattr(user, 'employee_profile'):
            return LeaveBalance.objects.filter(employee=user.employee_profile)
        return LeaveBalance.objects.none()

class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    Employees can create requests and view their own.
    Managers/HR can approve/reject.
    """
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LeaveRequest.objects.all()
        if hasattr(user, 'employee_profile'):
            return LeaveRequest.objects.filter(employee=user.employee_profile)
        return LeaveRequest.objects.none()

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.employee_profile)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve_manager(self, request, pk=None):
        leave_request = self.get_object()
        serializer = LeaveApproveSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['action'] == 'APPROVE':
                leave_request.status = LeaveRequest.Status.APPROVED_BY_MANAGER
                leave_request.manager_approver = request.user
            else:
                leave_request.status = LeaveRequest.Status.REJECTED
                leave_request.manager_approver = request.user
            leave_request.save()
            return Response(LeaveRequestSerializer(leave_request).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
