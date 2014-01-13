from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('ui.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^bike/(?P<bike_id>[0-9]+)/', 'bike', name='bike'),
    url(r'^station/(?P<station_id>[0-9]+)/$', 'station', name='station'),
    url(r'^station/(?P<station_id>[0-9]+)/stats/$', 'station_stats',
        name='station_stats'),
    url(r'^station/(?P<station_id>[0-9]+)/monthly_summary.json',
        'station_monthly_summary_json', name='station_monthly_summary_json'),
    url(r'^from/(?P<station_start_id>[0-9]+)/to/(?P<station_end_id>[0-9]+)/',
        'from_to_station', name='from_to_station'),
)
