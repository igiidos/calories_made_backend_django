# Generated by Django 3.2.6 on 2022-06-06 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calories', '0018_alter_weightandphoto_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='weightandphoto',
            name='photo_full_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
