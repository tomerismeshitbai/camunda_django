from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="Документация API для фронтенда",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("camunda_api.urls")),
    path("api/", include("dean_managers.urls")),
    path('api/faq/', include('faq.urls')),
    path('api/faq-requests/', include('faq_requests.urls')),
    path("api/students/", include("students.urls")),
    path("api/document_samples/", include("document_samples.urls")),

  
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)