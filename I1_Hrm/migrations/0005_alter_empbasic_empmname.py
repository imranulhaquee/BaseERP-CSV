# Generated by Django 4.1.1 on 2023-05-02 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('I1_Hrm', '0004_alter_empbasic_empmname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empbasic',
            name='empMName',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
