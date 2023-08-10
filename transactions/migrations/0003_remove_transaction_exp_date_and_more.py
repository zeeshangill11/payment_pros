# Generated by Django 4.1.7 on 2023-06-23 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_remove_transaction_account_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='exp_date',
        ),
        migrations.AddField(
            model_name='transaction',
            name='Transaction_id',
            field=models.CharField(default='', max_length=5, verbose_name='Transaction_id'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='exp_month',
            field=models.CharField(default='', max_length=5, verbose_name='Expiration Month'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='exp_year',
            field=models.CharField(default='', max_length=5, verbose_name='Expiration Year'),
        ),
    ]