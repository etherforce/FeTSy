# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fetsy', '0002_add_default_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='deadline',
        ),
        migrations.AddField(
            model_name='ticket',
            name='period',
            field=models.PositiveIntegerField(default=120, verbose_name='Period (in minutes)'),
            preserve_default=True,
        ),
    ]
