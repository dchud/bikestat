from django.contrib import admin

from ui import models as m


class RideAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_start', 'date_end', 'station_start',
                    'station_end', 'terminal_start', 'terminal_end',
                    'bike_num', 'status'
                    ]
    list_filter = ['status']
admin.site.register(m.Ride, RideAdmin)
