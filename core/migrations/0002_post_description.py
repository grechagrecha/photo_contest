# Generated by Django 4.2.7 on 2023-11-15 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(blank=True, default='There should have been a description, but it was not filled.', max_length=1000),
        ),
    ]
