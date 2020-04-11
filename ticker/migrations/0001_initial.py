# Generated by Django 3.0.4 on 2020-04-11 17:45

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ticker.utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('security_name', models.CharField(blank=True, max_length=300, null=True)),
                ('exchange', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'symbols',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('price', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('name', models.CharField(blank=True, max_length=80, null=True, unique=True)),
                ('sector', models.CharField(blank=True, max_length=90, null=True, unique=True)),
                ('industry', models.CharField(blank=True, max_length=90, null=True, unique=True)),
                ('previous_close', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('fifty_two_week_low', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('fifty_two_week_high', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('day_low', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('day_high', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('pe_ratio', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('eps', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('market_cap', models.BigIntegerField(blank=True, null=True)),
                ('exchange', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tickers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier', models.IntegerField(choices=[(1, 'NORMAL'), (2, 'PREMIUM'), (3, 'GOLD')], default=ticker.utils.utils.UserTier['NORMAL'])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profiles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticker.UserProfile')),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticker.Ticker')),
            ],
            options={
                'db_table': 'watch_lists',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_name', models.CharField(max_length=100, unique=True)),
                ('contract_type', models.CharField(max_length=1)),
                ('strike', models.DecimalField(decimal_places=10, max_digits=20)),
                ('iv', models.DecimalField(decimal_places=10, default=Decimal('0.00'), max_digits=20)),
                ('change', models.DecimalField(blank=True, decimal_places=10, default=Decimal('0.00'), max_digits=20, null=True)),
                ('volume', models.IntegerField(blank=True, default=0, null=True)),
                ('ask', models.DecimalField(decimal_places=10, default=Decimal('0.00'), max_digits=20)),
                ('bid', models.DecimalField(decimal_places=10, default=Decimal('0.00'), max_digits=20)),
                ('last_price', models.DecimalField(blank=True, decimal_places=10, default=Decimal('0.00'), max_digits=20, null=True)),
                ('expires', models.DateTimeField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticker.Ticker')),
            ],
            options={
                'db_table': 'options',
                'managed': True,
            },
        ),
    ]
