# Generated by Django 3.2.6 on 2021-09-03 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FitnessSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec', models.CharField(default='운동이름', max_length=100)),
                ('icon', models.CharField(blank=True, max_length=255, null=True)),
                ('calorie', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FitnessActivate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.PositiveIntegerField(default=0)),
                ('worked_at', models.DateTimeField(auto_now_add=True)),
                ('fitness', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='calories.fitnessspec')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
