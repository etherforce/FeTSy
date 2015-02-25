from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('name', models.CharField(verbose_name='Name', max_length=255, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name='Content')),
                ('assignee', models.ForeignKey(verbose_name='Assignee', null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(verbose_name='Status', to='fetsy.Status')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
