# Generated by Django 4.2.7 on 2024-01-27 17:54

import django_fsm
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0020_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='state',
            field=django_fsm.FSMField(choices=[('on_validation', 'On validation'), ('published', 'Published')],
                                      default=('on_validation', 'On validation'), max_length=50),
        ),
    ]
