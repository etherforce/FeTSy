from django.db import migrations, models
from django.utils.translation import ugettext_noop


def add_default_status(apps, schema_editor):
    # We can't import the Status model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Status = apps.get_model('fetsy', 'Status')
    status = []
    for name in (
        ugettext_noop('New'),
        ugettext_noop('Work in progress'),
        ugettext_noop('Closed')):
        status.append(Status(name=name))
    Status.objects.bulk_create(status)


class Migration(migrations.Migration):

    dependencies = [
        ('fetsy', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_status),
    ]
