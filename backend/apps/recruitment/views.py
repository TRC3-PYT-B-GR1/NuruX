from rest_framework import permissions, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.common.permissions import IsManagerOrHR
from .models import Candidate, JobPosting
from .serializers import CandidateSerializer, JobPostingSerializer, PublicApplicationSerializer


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


class PublicJobListView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        jobs = JobPosting.objects.filter(status=JobPosting.Status.OPEN)
        return Response(JobPostingSerializer(jobs, many=True).data)


class PublicJobDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request, pk):
        job = get_object_or_404(JobPosting, pk=pk, status=JobPosting.Status.OPEN)
        return Response(JobPostingSerializer(job).data)


class PublicApplicationView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    parser_classes = [MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, pk):
        job = get_object_or_404(JobPosting, pk=pk, status=JobPosting.Status.OPEN)
        serializer = PublicApplicationSerializer(data=request.data, context={"job": job})
        serializer.is_valid(raise_exception=True)
        candidate = serializer.save(job=job, stage="applied", score=0)
        return Response({"id": candidate.id, "message": "Application received. Our team will be in touch."}, status=status.HTTP_201_CREATED)
