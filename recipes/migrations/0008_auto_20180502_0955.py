# Generated by Django 2.0.3 on 2018-05-02 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20180408_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacy',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pharmacy',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicinerequest',
            name='apothecary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recipes.Apothecary'),
        ),
        migrations.AlterField(
            model_name='medicinerequest',
            name='given_medicine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recipes.Medicine'),
        ),
        migrations.AlterField(
            model_name='medicinerequest',
            name='request_confirmation_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='medicine_card_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='medicine_policy_number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]