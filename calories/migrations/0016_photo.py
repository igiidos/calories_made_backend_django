# Generated by Django 3.2.6 on 2022-06-06 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calories', '0015_weightandphoto_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
