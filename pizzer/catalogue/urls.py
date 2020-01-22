from django.urls import path

from catalogue.api import CurrencyApi


urlpatterns = [
    path('currency/', CurrencyApi.as_view()),
]
