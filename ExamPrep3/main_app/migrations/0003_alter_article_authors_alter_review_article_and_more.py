# Generated by Django 4.2.14 on 2024-07-29 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_author_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='authors',
            field=models.ManyToManyField(related_name='articles', to='main_app.author'),
        ),
        migrations.AlterField(
            model_name='review',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main_app.article'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main_app.author'),
        ),
    ]
