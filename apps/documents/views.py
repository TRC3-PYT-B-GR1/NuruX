from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from apps.audit.services import log_action
from apps.employees.permissions import FULL_WRITE_ROLES, get_visible_employees

from .models import EmployeeDocument
from .permissions import DocumentPermission, get_document_queryset_for_user
from .serializers import EmployeeDocumentSerializer


class _EmployeeScopedMixin:
    def get_employee(self):
        employee_id = self.kwargs["employee_id"]
        visible = get_visible_employees(self.request.user)
        return get_object_or_404(visible, pk=employee_id)


class EmployeeDocumentListCreateView(_EmployeeScopedMixin, generics.ListCreateAPIView):
    """
    GET  /api/v1/employees/{employee_id}/documents/
    POST /api/v1/employees/{employee_id}/documents/   (multipart, for `file`)
    """

    serializer_class = EmployeeDocumentSerializer
    permission_classes = [DocumentPermission]

    def get_queryset(self):
        employee = self.get_employee()
        return get_document_queryset_for_user(self.request.user).filter(employee=employee)

    def perform_create(self, serializer):
        employee = self.get_employee()
        user = self.request.user

        if not (user.is_superuser or user.role in FULL_WRITE_ROLES):
            # DocumentPermission.has_permission already confirmed the user's
            # ROLE can write at all; this enforces the row-level "own team,
            # no confidential" rule specifically for Managers.
            if user.role != "manager":
                raise PermissionDenied("You do not have permission to upload documents for this employee.")
            visible_ids = set(get_visible_employees(user).values_list("id", flat=True))
            if employee.id not in visible_ids:
                raise PermissionDenied("You can only upload documents for your own team.")
            if serializer.validated_data.get("sensitivity") == EmployeeDocument.Sensitivity.CONFIDENTIAL:
                raise PermissionDenied("Managers cannot upload confidential documents — HR/Admin only.")

        # Versioning: superseding any existing "current" document of the same type.
        previous = EmployeeDocument.objects.filter(
            employee=employee,
            document_type=serializer.validated_data["document_type"],
            is_current=True,
        ).first()

        version_number = 1
        supersedes = None
        if previous:
            previous.is_current = False
            previous.save(update_fields=["is_current"])
            version_number = previous.version_number + 1
            supersedes = previous

        serializer.save(
            employee=employee,
            uploaded_by=user,
            version_number=version_number,
            supersedes=supersedes,
            is_current=True,
        )


class EmployeeDocumentDetailView(_EmployeeScopedMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PATCH/DELETE /api/v1/employees/{employee_id}/documents/{id}/
    DELETE archives the record — see EmployeeDocument's docstring.
    """

    serializer_class = EmployeeDocumentSerializer
    permission_classes = [DocumentPermission]

    def get_queryset(self):
        employee = self.get_employee()
        return get_document_queryset_for_user(self.request.user).filter(employee=employee)

    def perform_destroy(self, instance):
        instance.is_archived = True
        instance.save(update_fields=["is_archived"])
        log_action(
            actor=self.request.user,
            action="document.archived",
            target=instance,
            changes={"document_type": instance.document_type, "sensitivity": instance.sensitivity},
            request=self.request,
        )


class EmployeeDocumentDownloadView(_EmployeeScopedMixin, APIView):
    """
    GET /api/v1/employees/{employee_id}/documents/{id}/download/

    Streams the file only after the same DocumentPermission check every
    other endpoint uses — this is the "check permission before streaming,
    don't rely on an unguessable URL" endpoint the NFRs call for.

    IMPORTANT CAVEAT (see settings.py / this phase's writeup): if
    django.conf.urls.static() is still serving MEDIA_URL publicly (as
    configured for local dev in Phase 4), the raw file is ALSO reachable
    directly at that URL with no permission check at all — this endpoint
    does not close that hole by itself. Do not rely on it in production;
    see the note in config/urls.py.
    """

    permission_classes = [DocumentPermission]

    def get(self, request, employee_id, pk):
        employee = self.get_employee()
        document = get_object_or_404(
            get_document_queryset_for_user(request.user).filter(employee=employee), pk=pk
        )
        self.check_object_permissions(request, document)

        if not document.file:
            raise Http404("No file attached to this document record.")

        return FileResponse(
            document.file.open("rb"),
            as_attachment=True,
            filename=document.file.name.rsplit("/", 1)[-1],
        )
