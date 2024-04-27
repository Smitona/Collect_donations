from django.urls import include, path
from django.veiws.decorators.cache import cache_page
from rest_framework.routers import SimpleRouter

from api.views import CollectViewSet, PaymentViewSet


router = SimpleRouter()

app_name = 'api'

router.register(
    r'collects/(?P<collect_id>\d+)',
    cache_page(120)(CollectViewSet),
    basename='collects'
)

router.register(
    r'collects/(?P<collect_id>\d+)/payments/',
    cache_page(120)(PaymentViewSet),
    basename='payments'
)

urlpatterns = [
    path('', include(router.urls)),
]
