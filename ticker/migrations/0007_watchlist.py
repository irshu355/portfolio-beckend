# Generated by Django 3.0.4 on 2020-03-22 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticker', '0006_auto_20200321_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticker.Ticker')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'watch_list',
                'managed': True,
            },
        ),
    ]
