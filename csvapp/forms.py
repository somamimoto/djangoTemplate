from django import forms
from django.core.validators import FileExtensionValidator


class CsvFileUploadForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'], message='Invalid file')], required=True)
    has_header = forms.ChoiceField(widget=forms.RadioSelect, choices=[('True', 'Yes'), ('False', 'No')], required=False)


class CsvFileExportForm(forms.Form):
    select_data = forms.ChoiceField(widget=forms.RadioSelect, choices=[('product_data', 'Product Data'), ('saleshistory_data', 'Sales History Data')])
