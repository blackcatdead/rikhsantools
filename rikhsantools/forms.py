from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, TextInput, NumberInput, EmailInput, Select, PasswordInput, FileInput, ImageField, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rikhsantools.models import Imagetopdf, Pdfscombine


class FileForm(forms.ModelForm):
    class Meta:
        model = Imagetopdf
        fields = ('image', )

class PdfscombineForm(forms.ModelForm):
    class Meta:
        model = Pdfscombine
        fields = ('pdf', )

# class UploadFileForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     file = forms.FileField()