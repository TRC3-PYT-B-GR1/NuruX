# from rest_framework import filters, viewsets

# from apps.common.permissions import IsAdminOrHR

# from .models import CertificationType, Skill
# from .serializers import CertificationTypeSerializer, SkillSerializer


# class SkillViewSet(viewsets.ModelViewSet):
#     """CRUD for the Skill catalog. Admin/HR only."""

#     queryset = Skill.objects.all()
#     serializer_class = SkillSerializer
#     permission_classes = [IsAdminOrHR]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["name", "category"]
#     ordering_fields = ["name", "created_at"]


# class CertificationTypeViewSet(viewsets.ModelViewSet):
#     """CRUD for the CertificationType catalog. Admin/HR only."""

#     queryset = CertificationType.objects.all()
#     serializer_class = CertificationTypeSerializer
#     permission_classes = [IsAdminOrHR]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["name", "issuing_body", "category"]
#     ordering_fields = ["name", "created_at"]

from rest_framework import filters, viewsets

from apps.common.permissions import IsAdminOrHR

from .models import CertificationType, Skill
from .serializers import CertificationTypeSerializer, SkillSerializer


class SkillViewSet(viewsets.ModelViewSet):
    """CRUD for the Skill catalog. Admin/HR only."""

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminOrHR]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category"]
    ordering_fields = ["name", "created_at"]


class CertificationTypeViewSet(viewsets.ModelViewSet):
    """CRUD for the CertificationType catalog. Admin/HR only."""

    queryset = CertificationType.objects.all()
    serializer_class = CertificationTypeSerializer
    permission_classes = [IsAdminOrHR]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "issuing_body", "category"]
    ordering_fields = ["name", "created_at"]