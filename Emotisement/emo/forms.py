# Emotisement/forms.py

from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']
        widgets = {
            'video_file': forms.FileInput(attrs={'accept': '.mp4'}),
        }
