# Generated by Django 4.1.1 on 2023-04-26 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('I1_Hrm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empextra',
            name='empBank',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='empextra',
            name='empEmail',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
    ]
