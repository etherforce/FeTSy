from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fetsy', '0004_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='reminder',
            field=models.PositiveIntegerField(verbose_name='Remind me in ... minutes', default=120),
            preserve_default=True,
        ),
    ]
