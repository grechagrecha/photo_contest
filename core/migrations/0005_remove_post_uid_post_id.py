# Generated by Django 4.2.7 on 2023-11-16 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_id_post_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='uid',
        ),
        migrations.AddField(
            model_name='post',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
