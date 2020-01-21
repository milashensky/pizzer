from django.contrib import admin
from catalogue.models import Photo, Currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "rate", )


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("photo",)


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Currency, CurrencyAdmin)
