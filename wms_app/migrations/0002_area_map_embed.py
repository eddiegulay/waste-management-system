# Generated by Django 3.0.5 on 2023-06-16 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='map_embed',
            field=models.CharField(blank=True, max_length=9999, null=True),
        ),
    ]
