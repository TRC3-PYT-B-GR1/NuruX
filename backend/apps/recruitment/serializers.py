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

    class Meta:
        model = Candidate
        fields = ["id", "job", "job_title", "full_name", "email", "phone", "stage", "score", "applied"]
        read_only_fields = ["id", "job_title", "applied"]
