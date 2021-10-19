from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import permissions


app_name = 'app'


api = [
    path("auth/", include("app.authentication.urls", namespace="auth")),
    path("", include("app.surveys.urls", namespace="surveys")),
]

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/", include(api)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    schema_view = get_schema_view(
        openapi.Info(
            title="Survey App API",
            default_version='v1',
            description="API described here",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="nurmakhanow@gmail.com"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns += [
        path(
            "api/swagger/",
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui',
        ),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            path("__debug__/", include(debug_toolbar.urls))
        ]
