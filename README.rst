=======
 FeTSy
=======

FeTSy (Festival Ticketing System) is a small issue tracking system for mass
events. It is still under development.


Local development
-----------------

To setup a local development version run::

    $ virtualenv .virtualenv --python=python3
    $ source .virtualenv/bin/activate
    $ pip install --requirement requirements.txt
    $ npm install
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ sed -i 's/DEBUG = False/DEBUG = True/' fetsy_deployment/settings.py
    $ python manage.py runserver

To check coding styles run::

    $ pip install flake8 isort
    $ flake8 --exclude="fetsy/migrations/" manage.py fetsy
    $ isort --multi_line 3 --check-only --recursive manage.py fetsy


Deployment (Example)
--------------------

This is an example instruction for Ubuntu 14.04 using Apache HTTP
Server and PostgreSQL.

Install webserver, database and some requirements::

    $ sudo apt-get install python3-dev python-virtualenv
    $ sudo apt-get install npm nodejs-legacy
    $ sudo apt-get install apache2 libapache2-mod-wsgi-py3
    $ sudo apt-get install postgresql postgresql-server-dev-all
    $ sudo apt-get install git

Setup PostgreSQL user and database::

    $ sudo -u postgres createuser -P -d fetsy
    $ sudo -u postgres createdb -O fetsy fetsy

Remember the password you used here.

Get FeTSY and install requirements::

    $ git clone https://github.com/normanjaeckel/FeTSy
    $ cd FeTSy
    $ virtualenv .virtualenv --python=python3
    $ source .virtualenv/bin/activate
    $ pip install --requirement requirements.txt
    $ pip install psycopg2
    $ npm install
    $ python manage.py collectstatic

Edit fetsy_deployment/settings.py and update the ALLOWED_HOSTS entry and
the DATABASES entry as follows::

    ALLOWED_HOSTS = ['fetsy.example.com', 'www.fetsy.example.com']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'fetsy',
            'USER': 'fetsy',
            'PASSWORD': '...',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }

In ALLOWED_HOSTS use the domains where FeTSy should run. In database
password setting use instead of '...' the correct password you remembered
when creating the database user.

Edit fetsy_deployment/wsgi.py and uncomment all commented lines. Udate the
FETSY_HOME entry and use instead of '/path/to/FeTSy' the filesystem path to
where you cloned FeTSy.

Thereafter run::

    $ sudo chgrp www-data fetsy_deployment/settings.py
    $ chmod 640 fetsy_deployment/settings.py
    $ sudo chgrp www-data fetsy_deployment/changes.log
    $ python manage.py migrate
    $ python manage.py createsuperuser

Create as root a virtual host configuration file
/etc/apache2/sites-available/fetsy.conf with the following content::

    <VirtualHost *:80>
        ServerName fetsy.example.com
        ServerAlias www.fetsy.example.com
        ServerAdmin webmaster@fetsy.example.com

        Alias /static/ /path/to/FeTSy/fetsy_deployment/static/

        <Directory /path/to/FeTSy/fetsy_deployment/static/>
            Options None
            Require all granted
        </Directory>

        WSGIDaemonProcess fetsy user=www-data group=www-data threads=1
        WSGIProcessGroup fetsy
        WSGIScriptAlias / /path/to/FeTSy/fetsy_deployment/wsgi.py

        <Directory /path/to/FeTSy/fetsy_deployment>
            <Files wsgi.py>
                Options None
                Require all granted
            </Files>
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/fetsy.error.log
        CustomLog ${APACHE_LOG_DIR}/fetsy.access.log combined
    </VirtualHost>

Adapt correct domains  in the settings ServerName, ServerAlias and
ServerAdmin. Adapt the correct filesystem paths in the settings Alias,
Directory and WSGIScriptAlias.

Finally disable default virtual host, enable custom virtual host and
restart the webserver::

    $ sudo a2dissite 000-default
    $ sudo a2ensite fetsy
    $ sudo service apache2 restart
