from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('color_css_class', models.CharField(verbose_name='Color', max_length=255, choices=[('default', 'Grey'), ('primary', 'Dark blue'), ('success', 'Green'), ('info', 'Light blue'), ('warning', 'Yellow'), ('danger', 'Red')], default='default')),
                ('weight', models.IntegerField(verbose_name='Weight (for ordering', default=0, help_text='Tags with a higher weight appear behind other tags.')),
            ],
            options={
                'verbose_name': 'Tag',
                'ordering': ('weight',),
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('tags', models.TextField(blank=True, help_text='Separate tags with newline.', verbose_name='Tags')),
                ('status', models.PositiveIntegerField(verbose_name='Status', choices=[(1, 'New'), (2, 'Work in progress'), (3, 'Closed')], default=1)),
                ('priority', models.PositiveIntegerField(verbose_name='Priority', choices=[(1, 'Very low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very high')], default=3)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('period', models.PositiveIntegerField(verbose_name='Period (in minutes)', default=120)),
                ('assignee', models.ForeignKey(blank=True, null=True, verbose_name='Assignee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
            bases=(models.Model,),
        ),
    ]
