from rest_framework.routers import DefaultRouter

from django.urls import path

from .views import CandidateViewSet, JobPostingViewSet, PublicApplicationView, PublicJobDetailView, PublicJobListView

router = DefaultRouter()
router.register("jobs", JobPostingViewSet, basename="recruitment-job")
router.register("candidates", CandidateViewSet, basename="recruitment-candidate")

urlpatterns = [
    path("careers/jobs/", PublicJobListView.as_view(), name="public-careers-jobs"),
    path("careers/jobs/<int:pk>/", PublicJobDetailView.as_view(), name="public-careers-job-detail"),
    path("careers/jobs/<int:pk>/apply/", PublicApplicationView.as_view(), name="public-careers-apply"),
] + router.urls
