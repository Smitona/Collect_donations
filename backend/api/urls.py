from django.urls import include, path
from django.views.decorators.cache import cache_page
from rest_framework.routers import SimpleRouter

from api.views import CollectViewSet, PaymentViewSet


router = SimpleRouter()

app_name = 'api'

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
