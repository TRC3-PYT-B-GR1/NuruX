from rest_framework import serializers
from .models import Assessment, Certificate, Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        
class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__' 

    def validate_passing_score(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError('Passing score must be between 0 and 100.')
        return value
        
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__' 
