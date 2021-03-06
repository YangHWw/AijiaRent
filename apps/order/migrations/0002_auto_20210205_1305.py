# Generated by Django 2.2.17 on 2021-02-05 05:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('house', '0002_auto_20210205_1305'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.HouseInfo', verbose_name='房子'),
        ),
    ]
