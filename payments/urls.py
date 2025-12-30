from django.urls import path
from payments.views import PaymentCreateAPIView

app_name = "payments"

urlpatterns = [
    path("create/", PaymentCreateAPIView.as_view()),
]
