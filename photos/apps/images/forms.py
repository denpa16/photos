from django import forms
from .models import Image, Imagesize


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('url','title', 'image')
        labels = {
            "url": "Ссылка",
            "title": "Название изображения по ссылке",
            "image": "Файл"
        }

class ImagesizeForm(forms.ModelForm):
    class Meta:
        model = Imagesize
        fields = ('width', 'height')
        labels = {
            "width": "Ширина",
            "height": "Высота"
        }
