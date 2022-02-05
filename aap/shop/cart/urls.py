"""Product URLs."""
from django.urls import include, path
from rest_framework import routers

from .views import CartViewSet

router = routers.DefaultRouter()
router.register("", CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
