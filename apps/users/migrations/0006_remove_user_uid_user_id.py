# Generated by Django 4.2.7 on 2023-11-16 11:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_rename_id_user_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='uid',
        ),
        migrations.AddField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False,
                                      verbose_name='ID'),
            preserve_default=False,
        ),
    ]
