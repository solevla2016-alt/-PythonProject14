from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "paid_course",
        "paid_lesson",
        "payment_method",
    ]

    ordering_fields = [
        "payment_date",
    ]