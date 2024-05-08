from rest_framework import permissions, viewsets

from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404

from collect.models import Collect
from collect.serializers import (CollectListSerializer, CollectSerializer,
                                 FeedSerializer, PaymentSerializer)
from collect.tasks import send_collect_created, send_donation_created


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
        user_email = author.email
        send_collect_created.delay(user_email)

    def get_queryset(self):
        collects = Collect.objects.all().select_related('author')
        collects = collects.annotate(
            donators=Count('payments__donator'),
            collected=Sum('payments__amount')
        )
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
        send_donation_created.delay(user_email)

    def get_serializer_class(self):
        if self.action in ['post', 'patch', 'put']:
            return PaymentSerializer
        return FeedSerializer

    def get_queryset(self, *args, **kwargs):
        collect_id = self.kwargs.get('collect_id')

        collect = get_object_or_404(Collect, id=collect_id)
        return collect.payments.select_related('donator', 'donation_to')
