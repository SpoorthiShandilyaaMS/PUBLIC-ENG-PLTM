# Generated by Django 3.1.1 on 2020-12-04 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appdb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='qconst',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='qconst_name',
        ),
    ]
