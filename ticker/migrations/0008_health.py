# Generated by Django 3.0.4 on 2020-05-25 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticker', '0007_auto_20200506_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=500, null=True, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
