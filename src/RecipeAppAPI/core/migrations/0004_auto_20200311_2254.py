# Generated by Django 3.0.2 on 2020-03-11 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ingredient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='creator',
            new_name='user',
        ),
    ]
