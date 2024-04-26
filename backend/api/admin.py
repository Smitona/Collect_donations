from django.contrib import admin

from api.models import Collect, Payment


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'

@admin.register(Collect)
class CollectAdmin(BaseAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(BaseAdmin):
    pass
