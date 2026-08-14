from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/employees/", include("apps.employees.urls")),
    path("api/v1/employees/", include("apps.skills.employee_urls")),
    path("api/v1/employees/", include("apps.documents.urls")),
    path("api/v1/org/", include("apps.organizations.urls")),
    path("api/v1/catalog/", include("apps.skills.urls")),
    path("api/v1/audit/", include("apps.audit.urls")),
    # API documentation (drf-spectacular) — auto-generated from the
    # ViewSets/serializers above, not hand-maintained.
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    # Dev-only convenience so Django admin can preview uploaded files.
    #
    # SECURITY NOTE (Phase 5): this serves everything under MEDIA_URL
    # publicly, with NO permission check — anyone with a file's URL can
    # fetch it directly, bypassing DocumentPermission entirely. The
    # EmployeeDocumentDownloadView added in Phase 5 checks sensitivity/role
    # before streaming, but that protection is moot as long as this line
    # is active, since the same file is also reachable at /media/<path>/
    # unguarded. Before production:
    #   - remove this block, AND
    #   - move file storage to a private S3/Cloudinary bucket with signed,
    #     time-limited URLs (not public bucket URLs), so "guessing the path"
    #     isn't sufficient even outside Django's own serving.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
