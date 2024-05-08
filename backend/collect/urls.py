from django.urls import include, path
from rest_framework.routers import SimpleRouter

from collect.views import CollectViewSet, PaymentViewSet

router = SimpleRouter()

app_name = 'collect'

router.register(
    r'collects',
    CollectViewSet,
    basename='collects'
)

router.register(
    r'collects/(?P<collect_id>\d+)/payments',
    PaymentViewSet,
    basename='payments'
)

urlpatterns = [
    path('', include(router.urls)),
]
