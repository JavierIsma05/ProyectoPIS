# Generated by Django 3.2 on 2023-08-16 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='group',
        ),
    ]
