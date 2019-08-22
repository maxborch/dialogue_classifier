from django.core.validators import FileExtensionValidator
from django.forms import ModelForm, FileField, Form, ClearableFileInput

from catalogue.models import Upload


class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ['title', 'project', 'upload_date', 'comments']


class MediaForm(Form):
    valid_extensions = ('pdf', 'csv')

    files = FileField(help_text=f"Allowed formats: {valid_extensions}... Beware: Filenames must not contain spaces",
                      required=False, widget=ClearableFileInput(attrs={'multiple': True}),
                      validators=[FileExtensionValidator(valid_extensions)])
