from django.conf.urls import include, url
from django.contrib import admin

from refugee_manager import views

admin.autodiscover()

urlpatterns = [
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include(admin.site.urls)),
    url(r'^refugee_manager/', include('refugee_manager.urls')),
    url(r'^calendar/', include('swingtime.urls')),
    url(r'^uploads/(?P<filename>.*)$', views.serve_file),
]
