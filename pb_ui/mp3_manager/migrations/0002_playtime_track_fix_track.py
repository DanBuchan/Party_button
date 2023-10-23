# Generated by Django 4.2.6 on 2023-10-20 19:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp3_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seconds', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(600)])),
            ],
        ),
        migrations.AddField(
            model_name='track',
            name='fix_track',
            field=models.BooleanField(default=True),
        ),
    ]