# Generated by Django 3.1.1 on 2020-09-19 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_project', '0002_auto_20200918_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='change',
            field=models.DecimalField(decimal_places=2, default=0),
            preserve_default=False,
        ),
    ]