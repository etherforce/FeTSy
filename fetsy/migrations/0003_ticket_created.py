import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fetsy', '0002_add_default_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='created',
            field=models.DateTimeField(verbose_name='Created', auto_now_add=True, default=datetime.datetime(2015, 2, 27, 21, 20, 3, 457224, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
