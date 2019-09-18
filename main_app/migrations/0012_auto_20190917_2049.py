# Generated by Django 2.2.3 on 2019-09-17 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_wallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='id',
        ),
        migrations.AlterField(
            model_name='wallet',
            name='btc_balance',
            field=models.DecimalField(decimal_places=8, default=10000, max_digits=30),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='eth_balance',
            field=models.DecimalField(decimal_places=8, default=10000, max_digits=30),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]