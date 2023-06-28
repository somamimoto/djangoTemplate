from django import forms
from django.core.validators import FileExtensionValidator


class CsvFileUploadForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'], message='Invalid file')], required=True)
    has_header = forms.BooleanField(widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]), required=False)
