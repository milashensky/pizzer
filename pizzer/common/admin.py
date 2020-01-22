from django.contrib import admin
from common.models import Customer, DeliveryAddress


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "currency", "delivery_address")


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("customer", "address", "house", "appartaments")


admin.site.register(Customer, CustomerAdmin)
admin.site.register(DeliveryAddress, DeliveryAdmin)
