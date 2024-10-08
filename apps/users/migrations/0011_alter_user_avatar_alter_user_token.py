# Generated by Django 4.2.7 on 2024-02-15 12:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0010_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='images/avatars/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
