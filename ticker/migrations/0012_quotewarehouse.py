# Generated by Django 3.0.4 on 2020-05-26 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticker', '0011_userprofile_is_online'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteWareHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.DecimalField(decimal_places=10, max_digits=20)),
                ('high', models.DecimalField(decimal_places=10, max_digits=20)),
                ('low', models.DecimalField(decimal_places=10, max_digits=20)),
                ('close', models.DecimalField(decimal_places=10, max_digits=20)),
                ('symbol', models.CharField(max_length=30, unique=True)),
                ('volume', models.IntegerField()),
                ('timeStamp', models.DateTimeField()),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticker.Ticker')),
            ],
            options={
                'db_table': 'quotes_warehouse',
                'managed': True,
            },
        ),
    ]
