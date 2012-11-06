from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('ui.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/', direct_to_template, {'template': 'about.html'}, 
        name='about'),
    url(r'^bike/(?P<bike_num>[a-zA-Z0-9]+)/', 'bike', name='bike'),
)
