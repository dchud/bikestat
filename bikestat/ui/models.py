from motionless import DecoratedMap, AddressMarker

from django.db import models as m


class DateFilterable:

    def date(self, year, month, day):
        return self.events.filter(date__year=year, date__month=month,
                                  date__day=day).order_by('-date')


class Station(m.Model, DateFilterable):
    desc = m.TextField(default='', blank=True)

    def __unicode__(self):
        return '(%s) %s' % (self.id, self.desc)


class Bike(m.Model, DateFilterable):
    num = m.CharField(db_index=True, max_length=14)

    def __unicode__(self):
        return '(%s) %s' % (self.id, self.num)


class Ride(m.Model):
    SUBSCRIBER = REGISTERED = 'r'
    CASUAL = 'c'
    STATUS_CHOICES = [
        (REGISTERED, 'Registered'),
        (CASUAL, 'Casual'),
    ]
    date_start = m.DateTimeField(db_index=True)
    date_end = m.DateTimeField(db_index=True)
    station_start = m.ForeignKey(Station, related_name='rides_start')
    station_end = m.ForeignKey(Station, related_name='rides_end')
    bike = m.ForeignKey(Bike, related_name='rides')
    status = m.CharField(db_index=True, max_length=2,
                         choices=STATUS_CHOICES, default=REGISTERED)

    @property
    def duration_seconds(self):
        delta = self.date_end - self.date_start
        return delta.seconds

    @property
    def duration_minutes(self, total=False):
        return self.duration_seconds / 60

    @property
    def duration_hours(self):
        delta = self.date_end - self.date_start
        seconds = delta.seconds
        return seconds / (60 * 60.0)

    @property
    def map_url(self):
        dmap = DecoratedMap(size_x=200, size_y=200)
        if self.station_start == self.station_end:
            dmap.add_marker(AddressMarker('%s, Washington, DC' %
                            self.station_start.desc, color='blue', label='B'))
        else:
            dmap.add_marker(AddressMarker('%s, Washington, DC' %
                            self.station_start.desc, color='green', label='S'))
            dmap.add_marker(AddressMarker('%s, Washington, DC' %
                            self.station_end.desc, color='red', label='E'))
        return dmap.generate_url()


def ride_duration_histogram(rides):
    d = {}
    for r in rides.all():
        try:
            d[r.duration_minutes] += 1
        except KeyError:
            d[r.duration_minutes] = 1
    h = []
    for i in range(max(d.keys()) + 1):
        h.append({'duration': i, 'count': d.get(i, 0)})
    return h


class Event(m.Model):
    ride = m.ForeignKey(Ride, related_name='events')
    date = m.DateTimeField(db_index=True)
    station = m.ForeignKey(Station, related_name='events')
    bike = m.ForeignKey(Bike, related_name='events')
    is_end = m.BooleanField(db_index=True, default=False)


def multi_map(rides):
    contiguous = False
    bikes = set([r.bike.num for r in rides])
    if len(bikes) == 1:
        contiguous = True
    dmap = DecoratedMap(size_x=600, size_y=600)
    for i in range(len(rides)):
        ride = rides[i]
        if contiguous:
            dmap.add_marker(AddressMarker('%s, Washington, DC' %
                            ride.station_start.desc, color='white',
                            label=chr(65 + i)))
        else:
            dmap.add_marker(AddressMarker('%s, Washington, DC' %
                            ride.station_start.desc, color='green', label='S'))
            dmap.add_marker(AddressMarker('%s, Washington, DC' %
                            ride.station_end.desc, color='red', label='E'))
    return dmap.generate_url()
