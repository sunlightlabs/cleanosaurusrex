from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from thecleanest.resources import *

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'thecleanest.views.home', name='home'),
    # url(r'^thecleanest/', include('thecleanest.foo.urls')),
    # url(r'schedule/', 'schedule.views.current_schedule'),
    # url(r'schedule/assignments/', 'schedule.views.assignments'),
    # url(r'schedule/debits/', 'schedule.views.debits'),
    # url(r'schedule/credits/', 'schedule.views.credits'),
    url(r'^schedule', 'schedule.views.current_schedule'),
    url(r'^admin/', include(admin.site.urls)),
)

# API

namelessworker_res = NamelessWorkerResource()
assignment_res = AssignmentResource()
credit_res = CreditResource()
debit_res = DebitResource()
nudge_res = NudgeResource()

urlpatterns += patterns('',
    url(r'^api/', include(namelessworker_res.urls)),
    url(r'^api/', include(assignment_res.urls)),
    url(r'^api/', include(credit_res.urls)),
    url(r'^api/', include(debit_res.urls)),
    url(r'^api/', include(nudge_res.urls)),
)
