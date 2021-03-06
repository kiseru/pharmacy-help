# Generated by Django 2.0.3 on 2018-04-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20180407_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='patient_initials',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='day_duration',
            field=models.PositiveIntegerField(default=15),
        ),
    ]
