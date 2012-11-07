from motionless import DecoratedMap, AddressMarker

from django.db import models as m


class Ride(m.Model):
    date_start = m.DateTimeField(db_index=True)
    date_end = m.DateTimeField(db_index=True)
    station_start = m.TextField(db_index=True)
    station_end = m.TextField(db_index=True)
    terminal_start = m.TextField(db_index=True, default='', blank=True)
    terminal_end = m.TextField(db_index=True, default='', blank=True)
    bike_num = m.CharField(db_index=True, max_length=14)
    status = m.CharField(db_index=True, max_length=10)

    @property
    def duration_seconds(self):
        delta = self.date_end - self.date_start
        return delta.seconds

    @property
    def duration_minutes(self, total=False):
        return self.duration_seconds / 60

    @property
    def map_url(self):
        dmap = DecoratedMap(size_x=200, size_y=200)
        dmap.add_marker(AddressMarker('%s, Washington, DC' %
                        self.station_start, color='green', label='S'))
        dmap.add_marker(AddressMarker('%s, Washington, DC' %
                        self.station_end, color='red', label='E'))
        return dmap.generate_url()
