# Generated by Django 2.1.5 on 2019-02-09 16:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_case_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(('jpeg', 'jpg', 'png', 'gif', 'mp3', 'mp4', 'mpeg'))])),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Case')),
            ],
        ),
    ]
