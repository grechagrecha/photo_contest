# Generated by Django 4.2.7 on 2023-11-16 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_uid_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='id',
            new_name='uid',
        ),
    ]