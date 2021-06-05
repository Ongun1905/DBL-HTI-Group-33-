from django import forms
from .models import File

class UploadFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = ''
        self.fields['file'].help_text = ''

    class Meta:
        model = File
        fields = ('file',)

        widgets = {
            'file': forms.FileInput(attrs={'id': 'upload-file', 'class': 'custom-upload'})
        }
