from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fetsy', '0005_ticket_reminder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='reminder',
        ),
        migrations.AddField(
            model_name='ticket',
            name='deadline',
            field=models.PositiveIntegerField(default=120, verbose_name='Deadline (in minutes)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='priority',
            field=models.PositiveIntegerField(choices=[(1, 'Very low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very high')], default=3, verbose_name='Priority'),
            preserve_default=True,
        ),
    ]
