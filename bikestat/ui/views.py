from django.db.models import Count
from django.shortcuts import render  # , get_object_or_404

from ui.models import Ride


def home(request):
    qs_bikes = Ride.objects.values('bike_num')
    qs_bikes = qs_bikes.annotate(bcount=Count('bike_num'))
    qs_bikes = qs_bikes.order_by('-bcount')
    return render(request, 'home.html', {
        'qs_bikes': qs_bikes[:25],
    })


def bike(request, bike_num):
    rides = Ride.objects.filter(bike_num=bike_num).order_by('-date_start')
    return render(request, 'bike.html', {
        'bike_num': bike_num,
        'rides': rides[:10],
    })
