from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
)
from lms.models import Course


class PaymentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Оплата курса")
    def post(self, request):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
        )

        product = create_stripe_product(course)
        price = create_stripe_price(product, payment.amount)
        session = create_stripe_session(price)

        payment.stripe_session_id = session.id
        payment.payment_url = session.url
        payment.save()

        return Response(PaymentSerializer(payment).data)
