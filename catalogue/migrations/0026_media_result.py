# Generated by Django 2.1.7 on 2019-08-20 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0025_upload_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='result',
            field=models.CharField(default='--None--', max_length=10000, null=True),
        ),
    ]
