from rest_framework.routers import DefaultRouter

from .views import CandidateViewSet, JobPostingViewSet

router = DefaultRouter()
router.register("jobs", JobPostingViewSet, basename="recruitment-job")
router.register("candidates", CandidateViewSet, basename="recruitment-candidate")

urlpatterns = router.urls
