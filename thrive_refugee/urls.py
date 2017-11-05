from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from refugee_manager import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include(admin.site.urls)),
    url(r'^refugee_manager/', include('refugee_manager.urls')),
    url(r'^calendar/', include('swingtime.urls')),
    url(r'^uploads/(?P<filename>.*)$', views.serve_file),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
