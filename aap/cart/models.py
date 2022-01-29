"""Product models."""
from django.db import models
from django.core.validators import MinValueValidator
from polymorphic.models import PolymorphicModel
from account.models import User
from base.models import Base
from account.models import Address
from product.models import Product


class Cart(PolymorphicModel, Base):
    """Cart model."""

    user = models.ForeignKey(User, related_name="cart_user_product", on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Address, related_name="cart_delivery_address", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_product", on_delete=models.CASCADE)
    # product = models.PositiveIntegerField()
    # content = models.TextField()
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    # price = models.PositiveIntegerField()

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name
