# Generated by Django 4.1.1 on 2023-04-16 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('H1_Items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itmextra',
            name='itmLogo',
            field=models.ImageField(blank=True, null=True, upload_to='images/itmLogo'),
        ),
    ]
