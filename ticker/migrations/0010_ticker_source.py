# Generated by Django 3.0.4 on 2020-05-25 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticker', '0009_auto_20200525_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
