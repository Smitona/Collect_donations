from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions

from api.models import Collect
from api.serializers import (
    CollectSerializer, CollectListSerializer, PaymentSerializer
)
from api.tasks import send_donation_created, send_collect_created


class CollectViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
        user_email = author.email
        send_collect_created(user_email)

    def get_queryset(self):
        collects = Collect.objects.all().select_related('author')
        return collects

    def get_serializer_class(self):
        if self.action == 'list':
            return CollectListSerializer
        return CollectSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        collect_id = self.kwargs.get('collect_id')
        donation_to = get_object_or_404(Collect, id=collect_id)
        donator = self.request.user
        serializer.save(
            donator=donator,
            donation_to=donation_to
        )
        user_email = donator.email
        send_donation_created(user_email)

    def get_queryset(self, *args, **kwargs):
        collect_id = self.kwargs.get('collect_id')

        collect = get_object_or_404(Collect, id=collect_id)
        return collect.donation.select_related('donator', 'donation_to')
