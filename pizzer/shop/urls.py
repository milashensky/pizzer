from django.urls import path, re_path

from shop.api import ProductApi, CategoryApi


urlpatterns = [
    path('product/', ProductApi.as_view()),
    re_path(r'^product/(?P<slug>[\w\-]+)/$', ProductApi.as_view()),
    path('category/', CategoryApi.as_view()),
]
