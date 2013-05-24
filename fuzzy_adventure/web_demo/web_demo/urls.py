from django.conf.urls import patterns, include, url
from web_demo.settings import DEBUG

urlpatterns = patterns('',

     url(r'^QA_demo/$', 'views.home.welcome'),
     url(r'^QA_demo/train/$', 'views.train.serve'),
     url(r'^QA_demo/about/$', 'views.about.serve'),
     url(r'^QA_demo/contact/$', 'views.contact.serve'),
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if DEBUG:
    urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': 'static'}
    ))
