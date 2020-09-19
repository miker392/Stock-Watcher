# Generated by Django 3.1.1 on 2020-09-18 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_symbol', models.CharField(max_length=20)),
                ('last_checked', models.DateField()),
                ('last_price', models.DecimalField(decimal_places=2)),
                ('low', models.DecimalField(decimal_places=2)),
                ('high', models.DecimalField(decimal_places=2)),
            ],
        ),
    ]