from django.db.models import Count, Sum
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets

from api.models import Collect, Payment, User
from api.serializers import CollectSerializer, UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CollectViewSet(viewsets.ModelViewSet):
    serializer_class = CollectSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Collect.objects.all().annotate(
            donators=Count('payments__donator'),
            collected=Sum('payments__amount')
        ).select_related('author')


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        serializer.save(donator=self.request.user)

    