# Generated by Django 5.1.1 on 2024-09-27 19:16

import pgvector.django.halfvec
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_update_max_sim_for_halfvec'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageembedding',
            name='half_embedding',
        ),
        migrations.RemoveField(
            model_name='queryembedding',
            name='half_embedding',
        ),
        migrations.AlterField(
            model_name='pageembedding',
            name='embedding',
            field=pgvector.django.halfvec.HalfVectorField(dimensions=128),
        ),
        migrations.AlterField(
            model_name='queryembedding',
            name='embedding',
            field=pgvector.django.halfvec.HalfVectorField(dimensions=128, null=True),
        ),
    ]
