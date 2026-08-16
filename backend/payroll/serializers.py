from rest_framework import serializers
from .models import SalaryStructure, PayrollRun, Payslip

class SalaryStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructure
        fields = '__all__'

class PayrollRunSerializer(serializers.ModelSerializer):
    processed_by_name = serializers.CharField(source='processed_by.get_full_name', read_only=True)
    
    class Meta:
        model = PayrollRun
        fields = '__all__'
        read_only_fields = ['id', 'processed_by', 'is_finalized', 'created_at']

    def validate_month(self, value):
        if value.day != 1:
            raise serializers.ValidationError('Payroll month must use the first day of the month.')
        return value

class PayslipSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    month = serializers.DateField(source='payroll_run.month', read_only=True)
    
    class Meta:
        model = Payslip
        fields = '__all__'
        read_only_fields = [field.name for field in Payslip._meta.fields]
