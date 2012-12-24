import datetime
import gzip
from optparse import make_option
import re
import sys
import time
import traceback

from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from ui.models import Station, Bike, Ride

TEST_LIMIT = 10000

RE_TERMINAL = re.compile(r' \(([0-9]+)\)')


def dt_aware_from_str(dt_str):
    ts = time.mktime(time.strptime(dt_str, '%m/%d/%Y %H:%M'))
    dt = datetime.datetime.fromtimestamp(ts)
    return timezone.make_aware(dt, timezone.utc)


class Command(BaseCommand):
    help = 'Load one or more bikeshare data files'

    option_list = BaseCommand.option_list + (
        make_option('--empty', action='store_true', default=False,
                    dest='empty', help='empty the db first'),
    )
    option_list = BaseCommand.option_list + (
        make_option('--test', action='store_true', default=False,
                    dest='test', help='limit to a test load'),
    )

    def handle(self, *args, **options):
        if options.get('empty', False):
            print 'emptying out db first'
            qs = Ride.objects.all()
            print 'deleting %s ride(s)' % qs.count()
            cursor = connection.cursor()
            cursor.execute('DELETE FROM ui_ride')
            cursor.execute('ALTER SEQUENCE ui_ride_id_seq RESTART WITH 1')
            print 'done'
            # let me see that this happened before it scrolls away
            time.sleep(2)
        i = 0
        for fname in args:
            print 'loading:', fname
            if fname.endswith('.gz'):
                fp = gzip.open(fname)
            else:
                fp = open(fname)
            # skip first line with fieldnames
            fp.readline()
            for line in fp:
                vals = line.strip().split(',')
                if len(vals) == 7:
                    dur_str, dts_str, dte_str, station_start, station_end, \
                        bike_num, status = vals
                elif len(vals) == 10:
                    dur_str, dur_seconds, dts_str, station_start, \
                        terminal_start, dte_str, station_end, terminal_end, \
                        bike_num, status = vals
                try:
                    dts = dt_aware_from_str(dts_str)
                    dte = dt_aware_from_str(dte_str)
                except:
                    print traceback.print_exc()
                    sys.exit(0)
                terms_start = RE_TERMINAL.findall(station_start)
                if terms_start:
                    terminal_start = terms_start[0]
                    station_start = station_start[:-8]
                terms_end = RE_TERMINAL.findall(station_end)
                if terms_end:
                    terminal_end = terms_end[0]
                    station_end = station_end[:-8]
                station_start, created = Station.objects.get_or_create(
                    terminal=terminal_start, desc=station_start)
                if created:
                    print 'new station:', station_start.desc
                station_end, created = Station.objects.get_or_create(
                    terminal=terminal_end, desc=station_end)
                if created:
                    print 'new station:', station_end.desc
                bike, created = Bike.objects.get_or_create(num=bike_num)
                if created:
                    print 'new bike:', bike.num
                ride, created = Ride.objects.get_or_create(
                    date_start=dts,
                    date_end=dte,
                    station_start=station_start,
                    station_end=station_end,
                    bike=bike,
                    status=getattr(Ride, status.upper()),
                )
                i += 1
                if options.get('test', False):
                    if i == TEST_LIMIT:
                        print 'TEST_LIMIT reached:', TEST_LIMIT
                        fp.close()
                        sys.exit()
            fp.close()
