# Generated by Django 4.1.1 on 2023-04-16 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='itmBasic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itmCode', models.CharField(max_length=12, unique=True)),
                ('itmName', models.CharField(max_length=100)),
                ('opeQty', models.IntegerField(blank=True, default=0, null=True)),
                ('cloQty', models.IntegerField(blank=True, default=0, null=True)),
                ('itmActive', models.CharField(blank=True, max_length=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='itmExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itmCode', models.CharField(max_length=12, unique=True)),
                ('itmLogo', models.ImageField(blank=True, null=True, upload_to='images/supLogo')),
                ('uPrice', models.IntegerField(blank=True, default=0, null=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('supplier', models.CharField(blank=True, max_length=100, null=True)),
                ('barCode', models.CharField(blank=True, max_length=30, null=True)),
                ('uom', models.CharField(blank=True, max_length=30, null=True)),
                ('min', models.IntegerField(blank=True, default=0, null=True)),
                ('max', models.IntegerField(blank=True, default=0, null=True)),
                ('roQty', models.IntegerField(blank=True, default=0, null=True)),
                ('discount', models.IntegerField(blank=True, default=0, null=True)),
                ('taxable', models.CharField(blank=True, max_length=50, null=True)),
                ('input', models.IntegerField(blank=True, default=0, null=True)),
                ('output', models.IntegerField(blank=True, default=0, null=True)),
                ('bisUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('itmType', models.CharField(blank=True, max_length=50, null=True)),
                ('expiry', models.IntegerField(blank=True, default=0, null=True)),
                ('ref', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
