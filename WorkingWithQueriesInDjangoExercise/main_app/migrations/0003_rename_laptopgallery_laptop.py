# Generated by Django 4.2.13 on 2024-07-03 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_laptopgallery'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LaptopGallery',
            new_name='Laptop',
        ),
    ]