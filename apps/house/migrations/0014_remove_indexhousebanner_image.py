# Generated by Django 2.2.17 on 2021-02-09 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0013_auto_20210209_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indexhousebanner',
            name='image',
        ),
    ]
