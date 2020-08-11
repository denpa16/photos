from django.shortcuts import render
from django.http import HttpResponse, Http404
from . models import Image
from .forms import ImageForm

def index(request):
    images_list = Image.objects.all()
    return render(request, 'images/list.html', {'images_list': images_list})

def add_photo(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            return render(request, 'images/add_photo.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'images/add_photo.html', {'form': form})

def detail(request, image_name):
    a = Image.objects.all()
    try:
        a.image = image_name
    except:
        raise Http404('Нет фотки')
    return render(request, 'images/detail.html', {'photo_name': a})