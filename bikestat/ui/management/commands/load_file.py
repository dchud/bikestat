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

# modes represent each data column ordering
MODE_2010 = 0
MODE_2012a = 1
MODE_2012b = 2


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
    option_list = option_list + (
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
        stations = {}
        bikes = {}
        for fname in args:
            print 'loading:', fname
            if fname.endswith('.gz'):
                fp = gzip.open(fname)
            else:
                fp = open(fname)
            # skip first line with fieldnames
            first_line = fp.readline()
            mode = -1
            if first_line.startswith(
                    'Duration,Start date,End date,Start station'):
                # early, e.g. 2010
                mode = MODE_2010
                print 'loading %s 2010-style' % fname
            elif first_line.startswith(
                    'Duration,Duration(Sec),Start date,Start Station'):
                # mid, e.g. 2012 1st quarter
                mode = MODE_2012a
                print 'loading %s 2012a-style' % fname
            elif first_line.startswith(
                    'Duration,Start date,Start Station,End date'):
                # later, e.g. 2012 3rd quarter
                mode = MODE_2012b
                print 'loading %s 2012b-style' % fname
            else:
                print 'Unrecognized column order in %s:\n%s' % \
                    (fname, first_line)
                sys.exit(0)

            for line in fp:
                vals = line.strip().split(',')
                # values not always set
                terminal_start = terminal_end = ''
                if mode == 0:
                    dur_str, dts_str, dte_str, station_start_str, \
                        station_end_str, bike_num, status = vals
                elif mode == 1:
                    dur_str, dur_seconds, dts_str, station_start_str, \
                        terminal_start, dte_str, station_end_str, \
                        terminal_end, bike_num, status = vals
                elif mode == 2:
                    dur_str, dts_str, station_start_str, dte_str, \
                        station_end_str, bike_num, status = vals
                else:
                    print 'invalid column format/mode'
                    sys.exit()
                try:
                    dts = dt_aware_from_str(dts_str)
                    dte = dt_aware_from_str(dte_str)
                except:
                    print traceback.print_exc()
                    sys.exit(0)
                terms_start = RE_TERMINAL.findall(station_start_str)
                if terms_start:
                    terminal_start = terms_start[0]
                    station_start_str = station_start_str[:-8]
                terms_end = RE_TERMINAL.findall(station_end_str)
                if terms_end:
                    terminal_end = terms_end[0]
                    station_end_str = station_end_str[:-8]
                try:
                    station_start = stations[station_start_str]
                except KeyError:
                    station_start, created = Station.objects.get_or_create(
                        terminal=terminal_start, desc=station_start_str)
                    if created:
                        print 'new station:', station_start.desc
                        stations[station_start_str] = station_start
                try:
                    station_end = stations[station_end_str]
                except KeyError:
                    station_end, created = Station.objects.get_or_create(
                        terminal=terminal_end, desc=station_end_str)
                    if created:
                        print 'new station:', station_end.desc
                        stations[station_end_str] = station_end
                try:
                    bike = bikes[bike_num]
                except KeyError:
                    bike, created = Bike.objects.get_or_create(num=bike_num)
                    if created:
                        print 'new bike:', bike.num
                        bikes[bike_num] = bike
                ride = Ride(date_start=dts, date_end=dte,
                            station_start=station_start,
                            station_end=station_end, bike=bike,
                            status=getattr(Ride, status.upper()))
                ride.save()
                i += 1
                if options.get('test', False):
                    if i == TEST_LIMIT:
                        print 'TEST_LIMIT reached:', TEST_LIMIT
                        fp.close()
                        sys.exit()
            fp.close()
