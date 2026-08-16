from rest_framework import serializers
from .models import KPI, Goal, ManagerFeedback, PerformanceReview

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'
        
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        
class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = '__all__'

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
        
class ManagerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerFeedback
        fields = '__all__'

