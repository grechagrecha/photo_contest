# Generated by Django 4.2.7 on 2024-02-15 12:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0023_post_number_of_likes_alter_post_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='number_of_comments',
            field=models.IntegerField(default=0),
        ),
    ]
