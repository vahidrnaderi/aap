"""Cart views."""
from .serializers import CartSerializer
from .models import Cart
from base.views import BaseViewSet
from rest_framework import permissions, generics


class CartViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Cart view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Cart.objects.filter(is_deleted=False)
    serializer_class = CartSerializer
    alternative_lookup_field = "product"
