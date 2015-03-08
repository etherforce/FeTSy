=======
 FeTSy
=======

Run::

    $ virtualenv .virtualenv --python=python3
    $ source .virtualenv/bin/activate
    $ pip install --requirement requirements.txt
    $ npm install
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ sed -i 's/DEBUG = False/DEBUG = True/' fetsy_deployment/settings.py
    $ python manage.py runserver

Later run::

    $ pip install flake8 isort
    $ flake8 --exclude="fetsy/migrations/" manage.py fetsy
    $ isort --multi_line 3 --check-only --recursive manage.py fetsy
