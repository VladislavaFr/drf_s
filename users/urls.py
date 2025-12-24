from django.urls import path
from users.views import UserUpdateAPIView, PaymentListAPIView

app_name = "users"

urlpatterns = [
    path("<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
]
