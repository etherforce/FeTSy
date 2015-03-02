from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fetsy', '0003_ticket_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(primary_key=True, max_length=255, verbose_name='Name', serialize=False)),
                ('color_css_class', models.CharField(max_length=255, default='default', verbose_name='Color', choices=[('default', 'Grey'), ('primary', 'Dark blue'), ('success', 'Green'), ('info', 'Light blue'), ('warning', 'Yellow'), ('danger', 'Red')])),
                ('weight', models.IntegerField(help_text='Tags with a higher weight appear behind other tags.', verbose_name='Weight (for ordering', default=0)),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
                'ordering': ('weight',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ticket',
            name='tags',
            field=models.ManyToManyField(null=True, blank=True, to='fetsy.Tag', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
