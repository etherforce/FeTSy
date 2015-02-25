import os
import re
import sys

from django.utils.crypto import get_random_string

DEPLOYMENT_DIRECTORY_NAME = 'fetsy_deployment'


def create_deployment_dir():
    # Creates the deployment directory with settings and wsgi file if
    # inexistent.
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(os.path.join(base_dir, DEPLOYMENT_DIRECTORY_NAME)):
        # Create directory.
        os.makedirs(os.path.join(base_dir, DEPLOYMENT_DIRECTORY_NAME))

        # Create settings file.
        with open(os.path.join(
                base_dir,
                'fetsy',
                'default_settings.py')) as default_settings:
            secret_key = get_random_string(
                50,
                'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
            settings = re.sub(
                r"SECRET_KEY = ''",
                "SECRET_KEY = '%s'" % secret_key,
                default_settings.read())

            wsgi_app = '%s.wsgi.application' % DEPLOYMENT_DIRECTORY_NAME
            settings = re.sub(
                r"WSGI_APPLICATION = ''",
                "WSGI_APPLICATION = '%s'" % wsgi_app,
                settings)

            settings_path = os.path.join(
                os.path.join(base_dir, DEPLOYMENT_DIRECTORY_NAME),
                'settings.py')
            with open(settings_path, 'w') as new_settings:
                new_settings.write(settings)

        # Create wsgi file.
        with open(os.path.join(
                base_dir,
                'fetsy',
                'default_wsgi.py')) as default_wsgi:
            django_settings_module = '%s.settings' % DEPLOYMENT_DIRECTORY_NAME
            wsgi = re.sub(
                r"DJANGO_SETTINGS_MODULE = ''",
                "DJANGO_SETTINGS_MODULE = '%s'" % django_settings_module,
                default_wsgi.read())
            wsgi_path = os.path.join(
                os.path.join(base_dir, DEPLOYMENT_DIRECTORY_NAME),
                'wsgi.py')
            with open(wsgi_path, 'w') as new_wsgi:
                new_wsgi.write(wsgi)


if __name__ == "__main__":
    create_deployment_dir()

    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        '%s.settings' % DEPLOYMENT_DIRECTORY_NAME)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
