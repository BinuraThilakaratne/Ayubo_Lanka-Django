# Generated by Django 4.1.4 on 2023-03-13 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_places'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='time',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
