from django.urls import path

from .employee_link_views import (
    EmployeeCertificationDetailView,
    EmployeeCertificationListCreateView,
    EmployeeSkillDetailView,
    EmployeeSkillListCreateView,
)

urlpatterns = [
    path(
        "<int:employee_id>/skills/",
        EmployeeSkillListCreateView.as_view(),
        name="employee-skill-list",
    ),
    path(
        "<int:employee_id>/skills/<int:pk>/",
        EmployeeSkillDetailView.as_view(),
        name="employee-skill-detail",
    ),
    path(
        "<int:employee_id>/certifications/",
        EmployeeCertificationListCreateView.as_view(),
        name="employee-certification-list",
    ),
    path(
        "<int:employee_id>/certifications/<int:pk>/",
        EmployeeCertificationDetailView.as_view(),
        name="employee-certification-detail",
    ),
]
