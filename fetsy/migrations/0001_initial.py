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
                ('name', models.CharField(serialize=False, primary_key=True, verbose_name='Name', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, verbose_name='Name', max_length=255)),
                ('color_css_class', models.CharField(default='default', choices=[('default', 'Grey'), ('primary', 'Dark blue'), ('success', 'Green'), ('info', 'Light blue'), ('warning', 'Yellow'), ('danger', 'Red')], verbose_name='Color', max_length=255)),
                ('weight', models.IntegerField(help_text='Tags with a higher weight appear behind other tags.', default=0, verbose_name='Weight (for ordering')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'ordering': ('weight',),
                'verbose_name': 'Tag',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('priority', models.PositiveIntegerField(default=3, choices=[(1, 'Very low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very high')], verbose_name='Priority')),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True)),
                ('period', models.PositiveIntegerField(default=120, verbose_name='Period (in minutes)')),
                ('assignee', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, verbose_name='Assignee', blank=True)),
                ('status', models.ForeignKey(to='fetsy.Status', verbose_name='Status')),
                ('tags', models.ManyToManyField(blank=True, null=True, to='fetsy.Tag', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
