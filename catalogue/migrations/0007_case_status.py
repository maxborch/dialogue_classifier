# Generated by Django 2.1.5 on 2019-02-09 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='status',
            field=models.CharField(choices=[('Pending Review', 'Pending Review'), ('Changes Required', 'Changes Required'), ('Live', 'Live')], default='Pending Review', max_length=99),
        ),
    ]
