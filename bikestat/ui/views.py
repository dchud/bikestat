from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from ui.models import Bike, Station, Ride


def home(request):
    qs_rides = Ride.objects.values('bike', 'bike__num')
    qs_rides = qs_rides.annotate(Count('bike'))
    qs_rides = qs_rides.order_by('-bike__count')
    return render(request, 'home.html', {
        'title': 'home',
        'rides': qs_rides[:50],
    })


def _paginate(request, paginator):
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return page, items


def bike(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    count = bike.events.count() / 2
    if count > 0:
        first = bike.events.order_by('date')[0]
    else:
        first = None
    longest = Ride.objects.raw('''
        SELECT *, MAX(date_end - date_start) AS the_max
        FROM ui_ride
        WHERE bike_id=%s
        GROUP BY id
        ORDER BY the_max DESC
        LIMIT 1''', [bike.id])
    paginator = Paginator(bike.events.order_by('-date'), 50)
    page, events = _paginate(request, paginator)
    return render(request, 'bike.html', {
        'title': 'bike %s' % bike.num,
        'bike': bike,
        'events': events,
        'count': count,
        'first': first,
        'longest': longest[0],
    })


def station(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    count = station.events.count()
    first = station.events.order_by('date')[0]
    paginator = Paginator(station.events.order_by('-date'), 50)
    page, events = _paginate(request, paginator)
    return render(request, 'station.html', {
        'title': station.desc,
        'station': station,
        'events': events,
        'count': count,
        'first': first,
    })


def from_to_station(request, station_start_id, station_end_id):
    station_start = get_object_or_404(Station, id=station_start_id)
    station_end = get_object_or_404(Station, id=station_end_id)
    qs_rides = station_start.rides_start.filter(station_end=station_end)
    count = qs_rides.count()
    first = qs_rides.order_by('date_start')[0]
    paginator = Paginator(qs_rides.order_by('-date_start'), 50)
    page, rides = _paginate(request, paginator)
    return render(request, 'from_to_station.html', {
        'title': 'from %s to %s' % (station_start.desc, station_end.desc),
        'station_start': station_start,
        'station_end': station_end,
        'rides': rides,
        'count': count,
        'first': first,
    })
