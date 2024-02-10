# Generated by Django 4.2.7 on 2024-01-31 14:24

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_post_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='state',
            field=django_fsm.FSMField(choices=[('on_validation', 'On validation'), ('published', 'Published')], default='on_validation', max_length=50),
        ),
    ]