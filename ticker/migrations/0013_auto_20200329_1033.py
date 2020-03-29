# Generated by Django 3.0.4 on 2020-03-29 14:33

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticker', '0012_auto_20200329_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='options',
            name='ask',
            field=models.DecimalField(decimal_places=20, default=Decimal('0.00'), max_digits=40),
        ),
        migrations.AlterField(
            model_name='options',
            name='bid',
            field=models.DecimalField(decimal_places=20, default=Decimal('0.00'), max_digits=40),
        ),
        migrations.AlterField(
            model_name='options',
            name='change',
            field=models.DecimalField(blank=True, decimal_places=20, default=Decimal('0.00'), max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='options',
            name='iv',
            field=models.DecimalField(decimal_places=20, default=Decimal('0.00'), max_digits=40),
        ),
        migrations.AlterField(
            model_name='options',
            name='last_price',
            field=models.DecimalField(blank=True, decimal_places=20, default=Decimal('0.00'), max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='day_high',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='day_low',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='eps',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='fifty_two_week_high',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='fifty_two_week_low',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='pe_ratio',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='previous_close',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True),
        ),
    ]
