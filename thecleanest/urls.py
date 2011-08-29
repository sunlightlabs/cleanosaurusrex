from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'thecleanest.views.home', name='home'),
    # url(r'^thecleanest/', include('thecleanest.foo.urls')),
    url(r'schedule/', 'schedule.views.current_schedule'),
    url(r'schedule/assignments/', 'schedule.views.assignments'),
    url(r'schedule/debits/', 'schedule.views.debits'),
    url(r'schedule/credits/', 'schedule.views.credits'),
    url(r'^admin/', include(admin.site.urls)),
)
