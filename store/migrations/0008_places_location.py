# Generated by Django 4.1.4 on 2023-03-13 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_places_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='Location',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
