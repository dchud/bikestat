from django.contrib import admin

from ui import models as m


class StationAdmin(admin.ModelAdmin):
    list_display = ['id', 'desc']
    search_fields = ['id', 'desc']
admin.site.register(m.Station, StationAdmin)


class BikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'num']
    search_fields = ['id', 'num']
admin.site.register(m.Bike, BikeAdmin)


class RideAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_start', 'date_end', 'station_start',
                    'station_end', 'bike', 'status'
                    ]
    list_filter = ['status']
admin.site.register(m.Ride, RideAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'station', 'bike', 'is_end']
    list_filter = ['is_end', 'station']
    search_fields = ['station', 'bike_num']
admin.site.register(m.Event, EventAdmin)
