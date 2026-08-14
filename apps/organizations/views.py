# from rest_framework import filters, viewsets

# from apps.common.permissions import IsAdminOrHR

# from .models import Department, Role
# from .serializers import DepartmentSerializer, RoleSerializer


# class DepartmentViewSet(viewsets.ModelViewSet):
#     """
#     CRUD for Department. Admin/HR only (see IsAdminOrHR).

#     Supports:
#       GET /org/departments/?search=finance
#       GET /org/departments/?ordering=-budget
#     """

#     queryset = Department.objects.select_related("manager", "parent_department").all()
#     serializer_class = DepartmentSerializer
#     permission_classes = [IsAdminOrHR]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["name"]
#     ordering_fields = ["name", "budget", "created_at"]

# class RoleViewSet(viewsets.ModelViewSet):
#     """
#     CRUD for Role. Admin/HR only.

#     Supports:
#       GET /org/roles/?search=officer
#       GET /org/roles/?department=3
#     """

#     queryset = Role.objects.select_related("department").all()
#     serializer_class = RoleSerializer
#     permission_classes = [IsAdminOrHR]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["title"]
#     ordering_fields = ["title", "created_at"]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         department_id = self.request.query_params.get("department")
#         if department_id:
#             queryset = queryset.filter(department_id=department_id)
#         return queryset


from rest_framework import filters, viewsets

from apps.common.permissions import IsAdminOrHR

from .models import Department, Role
from .serializers import DepartmentSerializer, RoleSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    CRUD for Department. Admin/HR only.
    """

    queryset = Department.objects.select_related(
        "manager",
        "parent_department",
    ).all()

    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrHR]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ["name"]

    ordering_fields = [
        "name",
        "budget",
        "created_at",
    ]

    ordering = ["name"]


class RoleViewSet(viewsets.ModelViewSet):
    """
    CRUD for Role. Admin/HR only.
    """

    queryset = Role.objects.select_related(
        "department",
    ).all()

    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrHR]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ["title"]

    ordering_fields = [
        "title",
        "created_at",
    ]

    ordering = ["title"]

    def get_queryset(self):
        queryset = super().get_queryset()

        department_id = self.request.query_params.get("department")

        if department_id:
            queryset = queryset.filter(
                department_id=department_id
            )

        return queryset