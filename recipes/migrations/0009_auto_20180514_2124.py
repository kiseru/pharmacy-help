# Generated by Django 2.0.4 on 2018-05-14 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20180514_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicinespharmacies',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='medicinespharmacies',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
