from django.urls import path

from common.api import ContextApi, CustomerApi, DeliveryAddressApi
from common.auth import LoginApi, LogoutApi, RegistrationApi


urlpatterns = [
    path('context/', ContextApi.as_view()),
    path('login/', LoginApi.as_view()),
    path('logout/', LogoutApi.as_view()),
    path('registration/', RegistrationApi.as_view()),
    path('customer/', CustomerApi.as_view()),
    path('address/', DeliveryAddressApi.as_view()),
]
