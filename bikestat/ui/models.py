from django.db import models as m


class Ride(m.Model):
    duration = m.IntegerField(default=0, db_index=True)
    date_start = m.DateTimeField(db_index=True)
    date_end = m.DateTimeField(db_index=True)
    station_start = m.TextField(db_index=True, blank=True)
    station_end = m.TextField(db_index=True, blank=True)
    terminal_start = m.TextField(db_index=True, blank=True)
    terminal_end = m.TextField(db_index=True, blank=True)
    bike_num = m.CharField(db_index=True, max_length=6)
    stats = m.CharField(db_index=True, max_length=10)
