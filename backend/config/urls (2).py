from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/employees/", include("apps.employees.urls")),
    path("api/v1/org/", include("apps.organizations.urls")), 
    path("api/v1/catalog/", include("apps.skills.urls")), 
]
