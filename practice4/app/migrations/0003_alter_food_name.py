# Generated by Django 5.1.6 on 2025-02-26 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_healthgoal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
