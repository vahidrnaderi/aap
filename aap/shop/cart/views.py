"""Cart views."""
from .serializers import CartSerializer
from .models import Cart
from shop.product.models import Product
# from shop.cart.serializers import CartPolymorphicSerializer
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

    # def list(self, request, *args, **kwargs):
    #     print

# class CartViewSet(
#     BaseViewSet,
#     generics.ListCreateAPIView,
#     generics.RetrieveAPIView,
#     generics.CreateAPIView,
# ):
#     """Cart view set."""
#
#     permission_classes = [permissions.DjangoModelPermissions]
#     queryset = Cart.objects.all()
#     serializer_class = CartPolymorphicSerializer
#     # alternative_lookup_field = "product"
