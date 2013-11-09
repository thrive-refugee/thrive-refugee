from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include(admin.site.urls)),
    url(r'^refugee_manager/', include('refugee_manager.urls')),
    url(r'^calendar/', include('swingtime.urls')),
)
