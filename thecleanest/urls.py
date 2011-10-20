from django.views.generic.simple import direct_to_template
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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^assignment/(?P<assignment_id>\d+)/$', 'schedule.views.assignment_detail', name='assignment_detail'),
    url(r'^assignment/(?P<defer_code>\w{32})/defer/$', 'schedule.views.defer_assignment'),
    url(r'^halloffame/$', 'schedule.views.hall_of_fame'),
    url(r'^hallofshame/$', 'schedule.views.hall_of_shame'),
    url(r'^full/$', 'schedule.views.full_schedule'),
    url(r'^kitchen/popover', direct_to_template, {'template': 'kitchen-popover.html'}),
    url(r'^kitchen', 'schedule.views.kitchen'),
    url(r'^schedule', 'schedule.views.current_schedule'),
    url(r'^worker/(?P<worker_id>\d+)/$', 'schedule.views.worker_detail', name='worker_detail'),
    url(r'^$', 'schedule.views.index'),
)

# API

namelessworker_res = NamelessWorkerResource()
assignment_res = AssignmentResource()
credit_res = CreditResource()
debit_res = DebitResource()
nudge_res = NudgeResource()
bone_res = BoneResource()

urlpatterns += patterns('',
    url(r'^api/', include(namelessworker_res.urls)),
    url(r'^api/', include(assignment_res.urls)),
    url(r'^api/', include(credit_res.urls)),
    url(r'^api/', include(debit_res.urls)),
    url(r'^api/', include(nudge_res.urls)),
    url(r'^api/', include(bone_res.urls)),
)
