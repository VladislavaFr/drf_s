from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/users/", include("users.urls", namespace="users")),
    path("api/lms/", include("lms.urls", namespace="lms")),
    path("api/payments/", include("payments.urls", namespace="payments")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
