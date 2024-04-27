from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404

from rest_framework.pagination import PageNumberPagination

from rest_framework import viewsets

from api.models import Collect, Payment, User
from api.serializers import (
    CollectSerializer, PaymentSerializer, UserSerializer
)
from api.tasks import send_donation_created, send_collect_created


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@staticmethod
def send(self, request, task):
    if request.method == 'POST':
        user_email = self.request.user.email
        task.delay(user_email)


class CollectViewSet(viewsets.ModelViewSet):
    serializer_class = CollectSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Collect.objects.all().annotate(
            donators=Count('payments__donator'),
            collected=Sum('payments__amount')
        ).select_related('author')

    def send_mail(self, request):
        return send(self, request, send_collect_created)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(donator=self.request.user)

    def get_queryset(self, *args, **kwargs):
        collect_id = self.kwargs.get('collect_id')

        collect = get_object_or_404(Collect, id=collect_id)
        return collect.donation.select_related('donator', 'donation_to')

    def send_mail(self, request):
        return send(self, request, send_donation_created)
