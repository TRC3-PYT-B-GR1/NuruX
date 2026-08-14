from django.urls import path

from .views import (
    EmployeeDocumentDetailView,
    EmployeeDocumentDownloadView,
    EmployeeDocumentListCreateView,
)

# Mounted at /api/v1/employees/ alongside apps.employees.urls and
# apps.skills.employee_urls — "/documents/" as a trailing segment doesn't
# collide with either of those (same reasoning as Phase 4).
urlpatterns = [
    path(
        "<int:employee_id>/documents/",
        EmployeeDocumentListCreateView.as_view(),
        name="employee-document-list",
    ),
    path(
        "<int:employee_id>/documents/<int:pk>/",
        EmployeeDocumentDetailView.as_view(),
        name="employee-document-detail",
    ),
    path(
        "<int:employee_id>/documents/<int:pk>/download/",
        EmployeeDocumentDownloadView.as_view(),
        name="employee-document-download",
    ),
]