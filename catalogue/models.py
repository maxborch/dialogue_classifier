import os
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


def name_file(instance, filename):
    return f'main_images/{instance.author}/{filename}'


def name_media_file(media, filename):
    return f'{settings.MEDIA_ROOT}/{media.upload.id}/{filename}'


# project
# class Disease(models.Model):
#     name = models.CharField(max_length=5000, null=True)
#     description = models.CharField(max_length=10000, null=True)
#     symptoms = models.CharField(max_length=5000, null=True)
#     categories = ()
#
#     category = models.CharField(max_length=99, choices=categories, default='Other')
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('disease-cases', kwargs={'disease_id': self.id})
#
#     class Meta:
#         ordering = ('name',)


class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    comments = models.CharField(max_length=10000, null=True)
    title = models.CharField(max_length=10000, null=True)
    result = models.CharField(max_length=10000, null=True, default="--None--")
    projects = (
        ('Create New Project', 'Create New Project'),
        ('Use existing project', 'Use existing project'),

    )
    project = models.CharField(max_length=99, choices=projects, default='--None--')

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('upload-detail', kwargs={'upload_id': self.id})


#######################################################################################################################

class Media(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    file = models.FileField(upload_to=name_media_file, validators=[FileExtensionValidator(('pdf', 'csv'))])
    result = models.CharField(max_length=10000, null=True, default="--None--")

    def file_type(self):
        other_extensions = ('.pdf', '.csv')

        name, extension = os.path.splitext(self.file.name)

        if extension in other_extensions:
            return 'other'

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension[1:]

    def filename(self):
        return os.path.basename(self.file.name)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
