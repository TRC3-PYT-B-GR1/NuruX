from rest_framework import serializers
from .models import LeaveBalance, LeaveRequest

class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = ['id', 'employee', 'leave_type', 'year', 'total_allocated', 'used_days', 'remaining_days']
        read_only_fields = ['id', 'employee', 'remaining_days']

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    manager_approver_name = serializers.CharField(source='manager_approver.get_full_name', read_only=True)
    hr_approver_name = serializers.CharField(source='hr_approver.get_full_name', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name', 'leave_type', 'start_date', 'end_date',
            'reason', 'status', 'manager_approver', 'manager_approver_name',
            'hr_approver', 'hr_approver_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'employee', 'status', 'manager_approver', 'hr_approver', 'created_at', 'updated_at']

class LeaveApproveSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['APPROVE', 'REJECT'])
