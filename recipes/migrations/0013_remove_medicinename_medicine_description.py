# Generated by Django 2.0.3 on 2018-05-24 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_recipe_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicinename',
            name='medicine_description',
        ),
    ]
