# Generated by Django 4.2.1 on 2023-05-08 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cardholder_name', models.CharField(max_length=255)),
                ('card_type', models.CharField(max_length=50)),
                ('account', models.CharField(max_length=50)),
                ('result', models.CharField(max_length=50)),
            ],
        ),
    ]
