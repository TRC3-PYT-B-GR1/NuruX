

from rest_framework.routers import DefaultRouter

from .views import CertificationTypeViewSet, SkillViewSet


router = DefaultRouter()

router.register("skills", SkillViewSet, basename="skill")
router.register(
    "certification-types",
    CertificationTypeViewSet,
    basename="certification-type",
)

urlpatterns = router.urls
