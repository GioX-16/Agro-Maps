# Generated by Django 5.0.6 on 2024-10-18 04:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0003_auto_20241016_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soilfertility',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapApp.location'),
        ),
    ]
