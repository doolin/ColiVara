# Generated by Django 5.1.1 on 2024-09-21 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_page_base64'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='base64',
            new_name='img_base64',
        ),
        migrations.AddField(
            model_name='document',
            name='base64',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]