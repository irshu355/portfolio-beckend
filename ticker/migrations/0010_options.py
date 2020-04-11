# Generated by Django 3.0.4 on 2020-03-29 03:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ticker', '0009_auto_20200322_0301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_name', models.CharField(max_length=100, unique=True)),
                ('contract_type', models.CharField(max_length=1)),
                ('strike', models.DecimalField(decimal_places=2, max_digits=8)),
                ('iv', models.DecimalField(decimal_places=2, max_digits=10)),
                ('change', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('ask', models.DecimalField(decimal_places=2, max_digits=8)),
                ('bid', models.DecimalField(decimal_places=2, max_digits=8)),
                ('last_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('expires', models.DateTimeField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticker.Ticker')),
            ],
        ),
    ]