from rest_framework import serializers

from .models import Candidate, JobPosting


class JobPostingSerializer(serializers.ModelSerializer):
    candidate_count = serializers.IntegerField(source="candidates.count", read_only=True)

    class Meta:
        model = JobPosting
        fields = ["id", "title", "description", "department", "status", "candidate_count", "date_posted"]
        read_only_fields = ["id", "candidate_count", "date_posted"]


class CandidateSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    applied = serializers.DateTimeField(source="applied_at", read_only=True)
    has_resume = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Candidate
        fields = ["id", "job", "job_title", "full_name", "email", "phone", "stage", "score", "has_resume", "applied"]
        read_only_fields = ["id", "job_title", "applied"]

    def get_has_resume(self, obj):
        return bool(obj.resume)


class PublicApplicationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Candidate
        fields = ["full_name", "email", "phone", "resume"]

    def validate_full_name(self, value):
        if len(value.strip().split()) < 2:
            raise serializers.ValidationError("Please provide your first and last name.")
        return value.strip()

    def validate(self, attrs):
        job = self.context["job"]
        if Candidate.objects.filter(job=job, email__iexact=attrs["email"]).exists():
            raise serializers.ValidationError("You have already applied for this position.")
        return attrs
