# Generated by Django 4.1.3 on 2025-07-04 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WeatherEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=100)),
                ("temperature", models.FloatField()),
                ("humidity", models.IntegerField()),
                ("icon", models.CharField(max_length=10)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
