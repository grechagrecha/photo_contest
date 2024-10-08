# Generated by Django 4.2.7 on 2023-11-26 22:31

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0012_alter_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, editable=False),
        ),
    ]
