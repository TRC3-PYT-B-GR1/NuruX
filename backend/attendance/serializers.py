from rest_framework import serializers
from .models import Attendance, Shift

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    shift_details = ShiftSerializer(source='shift', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'shift', 'shift_details',
            'date', 'clock_in', 'clock_out', 'status',
            'gps_location_in', 'gps_location_out', 'overtime_hours',
            'is_anomaly', 'anomaly_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'employee', 'date', 'clock_in', 'clock_out', 'status', 'overtime_hours', 'is_anomaly', 'anomaly_reason', 'created_at', 'updated_at']

class ClockInSerializer(serializers.Serializer):
    gps_location = serializers.CharField(required=True, max_length=255)

class ClockOutSerializer(serializers.Serializer):
    gps_location = serializers.CharField(required=True, max_length=255)
