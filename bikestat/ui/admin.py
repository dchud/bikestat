from django.contrib import admin

from ui import models as m


class RideAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_start', 'date_end', 'station_start',
                    'station_end', 'terminal_start', 'terminal_end',
                    'bike_num', 'status'
                    ]
    list_filter = ['status']
admin.site.register(m.Ride, RideAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'station', 'terminal', 'bike_num',
                    'is_end']
    list_filter = ['is_end', 'station']
    search_fields = ['station', 'terminal', 'bike_num']
admin.site.register(m.Event, EventAdmin)
