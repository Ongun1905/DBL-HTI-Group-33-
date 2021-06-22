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

#contactForm
class ContactForm(forms.Form):
    Your_Email = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
