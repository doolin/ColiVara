# Generated by Django 5.1.1 on 2024-11-03 01:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0022_base64_to_s3"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="document",
            name="base64",
        ),
    ]