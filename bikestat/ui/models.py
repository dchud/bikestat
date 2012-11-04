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
