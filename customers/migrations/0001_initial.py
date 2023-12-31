# Generated by Django 4.1.7 on 2023-06-02 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=20)),
                ('bill_company', models.CharField(max_length=100)),
                ('bill_first_name', models.CharField(max_length=50)),
                ('bill_last_name', models.CharField(max_length=50)),
                ('recurring_schedule', models.CharField(max_length=50)),
                ('bill_phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
