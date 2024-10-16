# Generated by Django 5.1.2 on 2024-10-15 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tenant",
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
                ("name", models.CharField(max_length=100)),
                ("domain", models.CharField(max_length=100, unique=True)),
                ("comment", models.TextField(blank=True)),
            ],
        ),
    ]
