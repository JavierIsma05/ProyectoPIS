# Generated by Django 4.2.4 on 2023-08-13 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='images',
            field=models.ImageField(default='users/users/default.png', upload_to='users/', verbose_name='Imagen de perfil'),
        ),
    ]