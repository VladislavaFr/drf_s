from django.urls import path
from users.views import UserUpdateAPIView

urlpatterns = [
    path("users/<int:pk>/", UserUpdateAPIView.as_view()),
]
