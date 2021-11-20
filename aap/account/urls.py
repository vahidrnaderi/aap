"""Auth URLs."""
from django.urls import path, include
from rest_framework import routers

from .views import (
    UserViewSet,
    GroupViewSet,
    PermissionViewSet,
    ContentTypeViewSet,
    LoginView,
    LogoutView,
    ChangePasswordView,
    MyProfileView,
    RegisterView,
)

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("groups", GroupViewSet, basename="group")
router.register("permissions", PermissionViewSet, basename="permission")
router.register("content_types", ContentTypeViewSet, basename="content_type")

urlpatterns = [
    path("", include(router.urls)),
    path("me/", MyProfileView.as_view(), name="me"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("password/", ChangePasswordView.as_view(), name="change_password"),
]
