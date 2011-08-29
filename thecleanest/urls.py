from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'thecleanest.views.home', name='home'),
    # url(r'^thecleanest/', include('thecleanest.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
