# Generated by Django 3.2.6 on 2022-06-06 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calories', '0019_weightandphoto_photo_full_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weightandphoto',
            name='save_date',
            field=models.DateField(),
        ),
    ]
