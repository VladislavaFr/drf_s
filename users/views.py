from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.serializers import (
    UserSerializer,
    PaymentSerializer,
    UserRegisterSerializer,
    UserPublicSerializer,
)
from users.permissions import IsOwnerProfile


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserSerializer
        return UserPublicSerializer

    permission_classes = [IsOwnerProfile]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerProfile]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "payment_course",
        "payment_lesson",
        "payment_method",
    )
    ordering_fields = ("payment_date",)
    ordering = ("payment_date",)
