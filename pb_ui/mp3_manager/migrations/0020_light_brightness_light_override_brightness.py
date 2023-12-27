# Generated by Django 4.2.6 on 2023-12-23 12:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp3_manager', '0019_discolight'),
    ]

    operations = [
        migrations.AddField(
            model_name='light',
            name='brightness',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='light',
            name='override_brightness',
            field=models.BooleanField(default=False),
        ),
    ]