# Generated by Django 2.2.28 on 2023-04-23 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heatsweep', '0007_auto_20230402_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tile',
            name='heat_value',
            field=models.CharField(default='#CCCCCC', max_length=7),
        ),
    ]
