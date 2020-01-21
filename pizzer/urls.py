from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/common/', include(('common.urls', 'common'), namespace='common')),
    path('api/shop/', include(('shop.urls', 'shop'), namespace='shop')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
]


if getattr(settings, 'DEBUG_TOOLBAR', None):
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
