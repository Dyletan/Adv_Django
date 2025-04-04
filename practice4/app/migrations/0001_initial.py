# Generated by Django 5.1.6 on 2025-02-25 10:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('carbs', models.FloatField(default=0)),
                ('fats', models.FloatField(default=0)),
                ('proteins', models.FloatField(default=0)),
                ('calorie', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Consume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('food_consumed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.food')),
            ],
        ),
    ]
