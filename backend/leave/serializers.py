from rest_framework import serializers
from django.utils import timezone
from .models import LeaveBalance, LeaveRequest

class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = ['id', 'employee', 'leave_type', 'year', 'total_allocated', 'used_days', 'remaining_days']
        read_only_fields = ['id', 'remaining_days']

    def validate(self, attrs):
        total = attrs.get('total_allocated', getattr(self.instance, 'total_allocated', 0))
        used = attrs.get('used_days', getattr(self.instance, 'used_days', 0))
        if used > total:
            raise serializers.ValidationError('Used days cannot exceed the total allocation.')
        return attrs

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    role_title = serializers.CharField(source='employee.role.title', read_only=True)
    manager_approver_name = serializers.CharField(source='manager_approver.get_full_name', read_only=True)
    hr_approver_name = serializers.CharField(source='hr_approver.get_full_name', read_only=True)
    duration_days = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name', 'department_name', 'role_title', 'leave_type', 'start_date', 'end_date',
            'reason', 'status', 'manager_approver', 'manager_approver_name',
            'hr_approver', 'hr_approver_name', 'duration_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'employee', 'status', 'manager_approver', 'hr_approver', 'created_at', 'updated_at']

    def get_duration_days(self, obj):
        return (obj.end_date - obj.start_date).days + 1

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError({'end_date': 'End date cannot be before start date.'})
            if start_date < timezone.localdate():
                raise serializers.ValidationError({'start_date': 'Leave cannot start in the past.'})
            if start_date.year != end_date.year:
                raise serializers.ValidationError('A leave request must stay within one calendar year.')

            request = self.context.get('request')
            employee = getattr(getattr(request, 'user', None), 'employee_profile', None)
            if employee:
                overlapping = LeaveRequest.objects.filter(
                    employee=employee,
                    start_date__lte=end_date,
                    end_date__gte=start_date,
                ).exclude(status__in=[LeaveRequest.Status.REJECTED, LeaveRequest.Status.CANCELLED])
                if self.instance:
                    overlapping = overlapping.exclude(pk=self.instance.pk)
                if overlapping.exists():
                    raise serializers.ValidationError('This request overlaps an existing leave request.')
        return attrs

class LeaveApproveSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['APPROVE', 'REJECT'])
