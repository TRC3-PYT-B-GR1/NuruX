from rest_framework import serializers
from .models import Attendance, Shift

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    shift_details = ShiftSerializer(source='shift', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    role_title = serializers.CharField(source='employee.role.title', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'department_name', 'role_title', 'shift', 'shift_details',
            'date', 'clock_in', 'clock_out', 'status',
            'gps_location_in', 'gps_location_out', 'overtime_hours',
            'is_anomaly', 'anomaly_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'employee', 'date', 'clock_in', 'clock_out', 'status', 'overtime_hours', 'is_anomaly', 'anomaly_reason', 'created_at', 'updated_at']

    def get_employee_name(self, obj):
        if obj.employee.user:
            full_name = obj.employee.user.get_full_name().strip()
            if full_name:
                return full_name
        return f'{obj.employee.first_name} {obj.employee.last_name}'.strip()


class GPSLocationSerializer(serializers.Serializer):
    gps_location = serializers.CharField(required=True, max_length=255)
    qr_token = serializers.CharField(required=True, help_text="Dynamic JWT from the QR kiosk")

    def validate_gps_location(self, value):
        try:
            latitude_text, longitude_text = (part.strip() for part in value.split(',', 1))
            latitude = float(latitude_text)
            longitude = float(longitude_text)
        except (TypeError, ValueError):
            raise serializers.ValidationError('Use latitude,longitude format.')
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            raise serializers.ValidationError('Coordinates are outside valid latitude/longitude ranges.')
        return f'{latitude:.6f},{longitude:.6f}'


class ClockInSerializer(GPSLocationSerializer):
    pass


class ClockOutSerializer(GPSLocationSerializer):
    pass
