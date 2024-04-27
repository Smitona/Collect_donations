from django.db.models import Count, Sum
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets

from api.models import Collect, Payment, User
from api.serializers import CollectSerializer, UserSerializer
from api.tasks import send_donation_created, send_collect_created

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    """
@staticmethod
def send_mail(self, request, task):
    if request.method == 'POST':
        user_email = self.request.user.email
        task.delay(user_email)"""


class CollectViewSet(viewsets.ModelViewSet):
    serializer_class = CollectSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Collect.objects.all().annotate(
            donators=Count('payments__donator'),
            collected=Sum('payments__amount')
        ).select_related('author')

    def send_mail(self, request):
        if request.method == 'POST':
            user_email = self.request.user.email
            send_collect_created.delay(user_email)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        serializer.save(donator=self.request.user)

    def send_mail(self, request):
        if request.method == 'POST':
            user_email = self.request.user.email
            send_donation_created.delay(user_email)
