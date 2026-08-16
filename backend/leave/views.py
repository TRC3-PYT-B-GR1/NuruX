from django.db import transaction
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsAdminOrHR
from .models import LeaveBalance, LeaveRequest
from .serializers import LeaveApproveSerializer, LeaveBalanceSerializer, LeaveRequestSerializer


class LeaveBalanceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Role-scoped leave balances; only HR/admin may allocate or adjust them."""

    serializer_class = LeaveBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_permissions(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return [permissions.IsAuthenticated(), IsAdminOrHR()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        queryset = LeaveBalance.objects.select_related('employee__department', 'employee__user')
        if user.is_superuser or user.role in {'super_admin', 'hr_officer', 'director'}:
            return queryset
        profile = getattr(user, 'employee_profile', None)
        if user.role == 'manager' and profile and profile.department_id:
            return queryset.filter(employee__department_id=profile.department_id)
        return queryset.filter(employee=profile) if profile else queryset.none()


class LeaveRequestViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Leave requests with explicit, auditable state-transition actions."""

    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = LeaveRequest.objects.select_related(
            'employee__department', 'employee__role', 'employee__user',
            'manager_approver', 'hr_approver',
        ).order_by('-created_at')
        if user.is_superuser or user.role in {'super_admin', 'hr_officer', 'director'}:
            scoped = queryset
        else:
            profile = getattr(user, 'employee_profile', None)
            if user.role == 'manager' and profile and profile.department_id:
                scoped = queryset.filter(employee__department_id=profile.department_id)
            else:
                scoped = queryset.filter(employee=profile) if profile else queryset.none()

        requested_status = self.request.query_params.get('status')
        if requested_status in LeaveRequest.Status.values:
            scoped = scoped.filter(status=requested_status)
        return scoped

    def create(self, request, *args, **kwargs):
        employee = getattr(request.user, 'employee_profile', None)
        if not employee:
            return Response({'detail': 'User has no employee profile.'}, status=400)
        if employee.status != employee.Status.ACTIVE:
            return Response({'detail': 'Only active employees can request leave.'}, status=403)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        duration = (end_date - start_date).days + 1
        balance = LeaveBalance.objects.filter(
            employee=employee,
            leave_type=serializer.validated_data['leave_type'],
            year=start_date.year,
        ).first()
        if not balance:
            return Response(
                {'leave_type': ['No leave balance has been allocated for this type and year.']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if balance.remaining_days < duration:
            return Response(
                {'detail': f'Insufficient leave balance: {balance.remaining_days} day(s) remaining.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(employee=employee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def approve_manager(self, request, pk=None):
        allowed_roles = {'manager', 'hr_officer', 'super_admin', 'director'}
        if not (request.user.is_superuser or request.user.role in allowed_roles):
            return Response({'detail': 'Manager approval permission required.'}, status=403)

        leave_request = self.get_queryset().select_for_update().get(pk=self.get_object().pk)
        if leave_request.status != LeaveRequest.Status.PENDING:
            return Response({'detail': 'Only pending requests can receive manager approval.'}, status=409)

        input_serializer = LeaveApproveSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        leave_request.manager_approver = request.user
        leave_request.status = (
            LeaveRequest.Status.APPROVED_BY_MANAGER
            if input_serializer.validated_data['action'] == 'APPROVE'
            else LeaveRequest.Status.REJECTED
        )
        leave_request.save(update_fields=['manager_approver', 'status', 'updated_at'])
        return Response(self.get_serializer(leave_request).data)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def approve_hr(self, request, pk=None):
        allowed_roles = {'hr_officer', 'super_admin', 'director'}
        if not (request.user.is_superuser or request.user.role in allowed_roles):
            return Response({'detail': 'HR approval permission required.'}, status=403)

        leave_request = self.get_queryset().select_for_update().get(pk=self.get_object().pk)
        if leave_request.status != LeaveRequest.Status.APPROVED_BY_MANAGER:
            return Response({'detail': 'Manager approval is required before HR review.'}, status=409)

        input_serializer = LeaveApproveSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        if input_serializer.validated_data['action'] == 'REJECT':
            leave_request.status = LeaveRequest.Status.REJECTED
        else:
            duration = (leave_request.end_date - leave_request.start_date).days + 1
            try:
                balance = LeaveBalance.objects.select_for_update().get(
                    employee=leave_request.employee,
                    leave_type=leave_request.leave_type,
                    year=leave_request.start_date.year,
                )
            except LeaveBalance.DoesNotExist:
                return Response({'detail': 'The employee has no matching leave balance.'}, status=409)
            if balance.remaining_days < duration:
                return Response({'detail': 'The employee no longer has sufficient leave balance.'}, status=409)
            balance.used_days += duration
            balance.save(update_fields=['used_days'])
            leave_request.status = LeaveRequest.Status.APPROVED_BY_HR

        leave_request.hr_approver = request.user
        leave_request.save(update_fields=['hr_approver', 'status', 'updated_at'])
        return Response(self.get_serializer(leave_request).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        leave_request = self.get_object()
        profile = getattr(request.user, 'employee_profile', None)
        if leave_request.employee_id != getattr(profile, 'id', None):
            return Response({'detail': 'You can only cancel your own leave request.'}, status=403)
        if leave_request.status != LeaveRequest.Status.PENDING:
            return Response({'detail': 'Only pending requests can be cancelled.'}, status=409)
        leave_request.status = LeaveRequest.Status.CANCELLED
        leave_request.save(update_fields=['status', 'updated_at'])
        return Response(self.get_serializer(leave_request).data)
