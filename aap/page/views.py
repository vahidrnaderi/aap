"""Page views."""
from base.views import BaseViewSet
from rest_framework import generics, permissions

from .models import GroupMenu, Menu, Page
from .serializers import GroupMenuSerializer, MenuSerializer, PageSerializer


class PageViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Page view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Page.objects.filter(is_deleted=False)
    serializer_class = PageSerializer


class MenuViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Menu view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Menu.objects.filter(is_deleted=False)
    serializer_class = MenuSerializer
    filterset_fields = ("label",)


class GroupMenuViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Group menu view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = GroupMenu.objects.filter(is_deleted=False)
    serializer_class = GroupMenuSerializer
    filterset_fields = ("name",)
