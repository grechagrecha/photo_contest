# Generated by Django 4.2.7 on 2023-11-23 23:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0008_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='images/posts/'),
        ),
    ]
