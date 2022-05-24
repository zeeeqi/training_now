# Generated by Django 4.0.4 on 2022-05-22 12:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_rename_user_bookings_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='dia',
        ),
        migrations.AddField(
            model_name='bookings',
            name='allow_inscriptions',
            field=models.BooleanField(default=True, verbose_name='Permitir inscripciones'),
        ),
        migrations.AddField(
            model_name='bookings',
            name='max_people',
            field=models.IntegerField(default=4, verbose_name='Maximo de personas'),
        ),
        migrations.AddField(
            model_name='bookings',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Inicio'),
            preserve_default=False,
        ),
    ]
