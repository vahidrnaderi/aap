"""Product URLs."""
from django.urls import include, path
from rest_framework import routers

from .views import CartSerializer

router = routers.DefaultRouter()
router.register("carts", CartSerializer, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
