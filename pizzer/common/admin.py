from django.contrib import admin
from common.models import Customer, DeliveryAddress


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "currency", "orders", "delivery_addresses")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", )
    save_on_top = True


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("customer", "details")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", )
    save_on_top = True


admin.site.register(Customer, CustomerAdmin)
admin.site.register(DeliveryAddress, DeliveryAdmin)
