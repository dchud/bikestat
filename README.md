bikestat
--------

A django app for futzin' with data from Capital Bikeshare, the
bikesharing network in Washington, DC, USA.

To get the data, go to http://capitalbikeshare.com/trip-history-data


installation
------------

These notes document how to get the app up and running with data loaded
using a clean Ubuntu 12.04 LTS machine.  You will need sudo rights.  You
can probably get it running easily elsewhere, but YMMV.


* Install apache and other dependencies:

        % sudo apt-get install apache2 libapache2-mod-wsgi python-dev libaio-dev git python-setuptools

* Install virtualenv and prep a directory to be a virtual environment
for the app, replacing "/BIKESTAT" with a directory location you
prefer, e.g. ' /home/dchud/apps/bikestat':

        % sudo easy_install virtualenv
        % mkdir /BIKESTAT
        % cd /BIKESTAT

* Clone the project code from github:

        % git clone https://github.com/dchud/bikestat.git

* Enter, create, and activate your virtual environment:

        % cd /BIKESTAT/bikestat
        % virtualenv ENV
        % source ENV/bin/activate

* Install key dependencies for the bikestat app:

        (ENV)% pip install -r requirements.txt
