from django.urls import path

from common.api import ContextApi, Users
from common.auth import LoginApi, LogoutApi, RegistrationApi


urlpatterns = [
    path('context', ContextApi.as_view()),
    path('login', LoginApi.as_view()),
    path('logout', LogoutApi.as_view()),
    path('registration', RegistrationApi.as_view()),
    path('users', Users.as_view()),
]
