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
                ('name', models.CharField(serialize=False, verbose_name='Name', primary_key=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(serialize=False, verbose_name='Name', primary_key=True, max_length=255)),
                ('color_css_class', models.CharField(default='default', verbose_name='Color', max_length=255, choices=[('default', 'Grey'), ('primary', 'Dark blue'), ('success', 'Green'), ('info', 'Light blue'), ('warning', 'Yellow'), ('danger', 'Red')])),
                ('weight', models.IntegerField(default=0, verbose_name='Weight (for ordering', help_text='Tags with a higher weight appear behind other tags.')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
                'ordering': ('weight',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('content', models.TextField(verbose_name='Content')),
                ('priority', models.PositiveIntegerField(default=3, verbose_name='Priority', choices=[(1, 'Very low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very high')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('deadline', models.PositiveIntegerField(default=120, verbose_name='Deadline (in minutes)')),
                ('assignee', models.ForeignKey(blank=True, verbose_name='Assignee', to=settings.AUTH_USER_MODEL, null=True)),
                ('status', models.ForeignKey(to='fetsy.Status', verbose_name='Status')),
                ('tags', models.ManyToManyField(to='fetsy.Tag', blank=True, null=True, verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
