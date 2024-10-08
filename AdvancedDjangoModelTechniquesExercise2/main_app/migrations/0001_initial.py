# Generated by Django 4.2.14 on 2024-07-11 12:29

import django.core.validators
from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[main_app.models.validate_name])),
                ('age', models.PositiveIntegerField(validators=[main_app.models.validate_age])),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(message='Enter a valid email address')])),
                ('phone_number', models.CharField(max_length=13, validators=[main_app.models.validate_phone_number])),
                ('website_url', models.URLField(validators=[django.core.validators.URLValidator(message='Enter a valid URL')])),
            ],
        ),
    ]
