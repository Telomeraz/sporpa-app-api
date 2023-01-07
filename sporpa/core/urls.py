from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/accounts/", include("accounts.api.v1.urls"), name="accounts"),
    path("api/v1/events/", include("events.api.v1.urls")),
    path("api/v1/participants/", include("participants.api.v1.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
