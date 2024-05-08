from collect.models import Collect, Payment
from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


@admin.register(Collect)
class CollectAdmin(BaseAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(BaseAdmin):
    pass
