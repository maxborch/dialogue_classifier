# Generated by Django 2.1.5 on 2019-02-09 17:41

import catalogue.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_case_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='image',
            field=models.ImageField(default='media/default_case.png', upload_to=catalogue.models.name_file),
        ),
    ]