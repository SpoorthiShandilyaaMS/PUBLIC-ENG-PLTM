# Generated by Django 3.1.1 on 2020-11-09 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdb', '0011_auto_20201109_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='query',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]