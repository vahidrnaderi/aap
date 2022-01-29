"""Cart serializers."""
from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    """Cart serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="cart:cart-detail")
    # total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            "url",
            "id",
            "user",
            "product",
            # "content",
            "quantity",
            # "price",
            # "total_price",
        )
        ref_name = "cart"

    # def get_total_price(self, obj):
    #     """Get post's star average."""
    #     if obj.price.all().aggregate(Avg("star"))["star__avg"]:
    #         return obj.stars.all().aggregate(Avg("star"))["star__avg"]
    #     else:
    #         return 0