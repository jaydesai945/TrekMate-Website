# Generated by Django 5.1 on 2024-09-25 07:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tour", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="check_in_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="booking",
            name="check_out_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]