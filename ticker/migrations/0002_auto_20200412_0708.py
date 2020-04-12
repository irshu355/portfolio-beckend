# Generated by Django 3.0.4 on 2020-04-12 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='ticker.UserProfile'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='ticker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='ticker.Ticker'),
        ),
    ]