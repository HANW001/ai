# Generated by Django 4.2.13 on 2024-06-03 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cafe24User",
            fields=[
                ("mall", models.CharField(max_length=255)),
                (
                    "id",
                    models.CharField(max_length=45, primary_key=True, serialize=False),
                ),
                ("password", models.CharField(max_length=255)),
                ("client_id", models.CharField(max_length=255)),
                ("client_secretkey", models.CharField(max_length=255)),
                ("servicekey", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "cafe24_user",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ImwebUser",
            fields=[
                (
                    "mall",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("id", models.CharField(max_length=255)),
                ("password", models.CharField(max_length=255)),
                ("api_key", models.CharField(max_length=255)),
                ("secret_key", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "imweb_user",
                "managed": False,
            },
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
