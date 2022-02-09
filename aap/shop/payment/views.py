"""Payment views."""
from .serializers import PaymentSerializer, OrderSerializer
from .models import Payment, Order
from base.views import BaseViewSet
from rest_framework import permissions, generics


class OrderViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Order view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Order.objects.filter(is_deleted=False)
    serializer_class = OrderSerializer
    alternative_lookup_field = "invoice_number"


class PaymentViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Order view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Payment.objects.filter(is_deleted=False)
    serializer_class = PaymentSerializer
    alternative_lookup_field = "invoice_number"

