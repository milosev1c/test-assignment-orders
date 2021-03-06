# Generated by Django 4.0.3 on 2022-03-21 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    This migration was created after revising the structure of the 'Order' model and it's connection to
    'OrderPart' model. M2M relation is not needed here.
    """
    dependencies = [
        ('assignment_orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='parts',
        ),
        migrations.AddField(
            model_name='orderpart',
            name='order',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='assignment_orders.order', verbose_name='Order'),
            preserve_default=False,
        ),
    ]
