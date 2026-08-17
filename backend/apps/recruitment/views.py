from rest_framework import viewsets

from apps.common.permissions import IsManagerOrHR
from .models import Candidate, JobPosting
from .serializers import CandidateSerializer, JobPostingSerializer


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsManagerOrHR]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.select_related("job").all()
    serializer_class = CandidateSerializer
    permission_classes = [IsManagerOrHR]
