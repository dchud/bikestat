from django.db.models import Count, Q
from django.shortcuts import render  # , get_object_or_404

from ui.models import Ride, multi_map


def home(request):
    qs_bikes = Ride.objects.values('bike_num')
    qs_bikes = qs_bikes.annotate(bcount=Count('bike_num'))
    qs_bikes = qs_bikes.order_by('-bcount')
    return render(request, 'home.html', {
        'title': 'home',
        'qs_bikes': qs_bikes[:10],
    })


def bike(request, bike_num):
    rides = Ride.objects.filter(bike_num=bike_num).order_by('-date_start')
    return render(request, 'bike.html', {
        'title': 'bike %s' % bike_num,
        'bike_num': bike_num,
        'rides': rides[:10],
        'multi_map_url': multi_map(rides[:10]),
    })


def station(request, desc):
    rides = Ride.objects.filter(Q(station_start=desc) | Q(station_end=desc))
    rides = rides.order_by('-date_start')
    return render(request, 'station.html', {
        'title': 'station %s' % desc,
        'rides': rides[:10],
        'desc': desc,
        'multi_map_url': multi_map(rides[:10]),
    })
