# Generated by Django 3.2.6 on 2022-05-26 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calories', '0006_atefoods'),
    ]

    operations = [
        migrations.RenameField(
            model_name='atefoods',
            old_name='unit_gram',
            new_name='unit',
        ),
    ]
