from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import (
    UserRegisterAPIView,
    UserRetrieveUpdateAPIView,
    UserListAPIView,
    UserDestroyAPIView,
    PaymentListAPIView,
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    path("", UserListAPIView.as_view(), name="user-list"),
    path("<int:pk>/", UserRetrieveUpdateAPIView.as_view(), name="user-detail"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),

    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
]
