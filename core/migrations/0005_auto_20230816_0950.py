# Generated by Django 3.2 on 2023-08-16 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_tutoria_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='firma',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='modalidad',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='time_quantity',
        ),
        migrations.AddField(
            model_name='tutoria',
            name='firma',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='firmas/'),
        ),
        migrations.AddField(
            model_name='tutoria',
            name='modalidad',
            field=models.CharField(choices=[('P', 'Presencial'), ('V', 'Virtual')], default='P', max_length=1, verbose_name='Modalidad'),
        ),
        migrations.AddField(
            model_name='tutoria',
            name='time_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Tiempo Empleado'),
        ),
        migrations.AlterField(
            model_name='tutoria',
            name='teacher',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'profesores'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Profesor'),
        ),
    ]
