# Generated by Django 3.2.6 on 2021-09-03 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('calories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessactivate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
    ]
