from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/",
        include(("lms.urls", "lms"), namespace="lms"),
    ),
    path(
        "api/",
        include(("users.urls", "users"), namespace="users"),
    ),
]
