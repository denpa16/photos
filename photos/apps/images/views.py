from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404
from . models import Image
from .forms import ImageForm, ImagesizeForm
import sqlite3 as lite
import urllib.request
import sys
import os
import django.db
from django.conf import settings
from PIL import Image as pimg

def index(request):
    images_list = Image.objects.all()
    a = []
    for i in range(len(images_list)):
        print(images_list[i].image.name)
    return render(request, 'images/list.html', {'images_list': images_list})

def add_photo(request):
    metka = True
    form = ImageForm()
    message = 'При загрузке изображения из сети необходимо дать ему название'
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        form.save(commit=False)
        img_obj = form.instance
        title = form.cleaned_data.get('title')
        img_url = form.cleaned_data.get('url')
        img_name = img_obj.image.name
        if img_name:
            images_list = Image.objects.all()
            for i in range(len(images_list)):
                if img_name == images_list[i].image.name:
                    form.save(commit=False)
                    form = ImageForm()
                    message = 'Изображение с таким именем файла уже существует. Переименуйте изображение на своем устройстве и загрузите его снова :)'
                    return render(request, 'images/add_photo.html', {'form': form, 'message': message})
                else:
                    form.save(commit=True)
            return redirect('/'+img_name)
        if img_url:
            if title:
                images_list = Image.objects.all()
                print('title =', title)
                for i in range(len(images_list)):
                    if (title + '.png') == images_list[i].image.name :
                        message = 'Изображение с таким именем файла уже существует. Переименуйте изображение и загрузите его снова :)'
                        metka = False
                        return render(request, 'images/add_photo.html', {'form': form, 'message': message})
                if metka == True:
                    print('Eps')
                    img = urllib.request.urlopen(img_url).read()
                    out = open(settings.MEDIA_ROOT + title +'.png', "wb")
                    out.write(img)
                    out.close
                    Image.objects.create(image = (title + '.png') )
                    return redirect('/'+(title + '.png'))
                        
            else:
                message = 'Фотографаия не загружена. Пожалуйста, дайте ей название'
                return render(request, 'images/add_photo.html', {'form': form, 'message': message})

        if (img_url == True) and (img_name == True):
            form.save(commit=False)
            message = 'Загружайте изображение либо только с компьютера, либо только из сети'
            return render(request, 'images/add_photo.html', {'form': form, 'message': message})
    else:
        form = ImageForm()
    return render(request, 'images/add_photo.html', {'form': form, 'message': message})

def detail(request, image_name):
    form = ImagesizeForm()
    if request.method == 'POST':
        form = ImagesizeForm(request.POST)
        form.save(commit=False)
        height = form.cleaned_data.get('height')
        width = form.cleaned_data.get('width')
        print(type(height))
        if width and height:
            height = int(form.cleaned_data.get('height'))
            width = int(form.cleaned_data.get('width'))
            print('true')
        if width == '':
            width = '0'
            height = int(height)
            width = int(width)
            print(type(width), width)
        if height == '':
            height = '0'
            height = int(height)
            width = int(width)
            print(type(height), height)

        image = pimg.open(os.path.normpath(settings.MEDIA_ROOT + image_name))
        (orig_width, orig_height) = image.size
        print(orig_width, orig_height)

        if (width != 0) and (height != 0):
            if height >= width:
                image = image.resize((width, round((orig_height/orig_width)*width)))
                (new_width, new_height) = image.size
                print('size', image.size)
            if height < width:
                image = image.resize((round((orig_width/orig_height)*height), height))
                (new_width, new_height) = image.size
                print('size',image.size)

        elif (width != 0) and (height == 0):
            if width >= orig_width:
                image = image.resize((orig_width, round((orig_height/orig_width)*width)))
                (new_width, new_height) = image.size
                new_height = orig_height
                print('size1', new_width, new_height)
            else:
                image = image.resize((width, round((orig_height/orig_width)*width)))
                (new_width, new_height) = image.size
                print('size2', new_width, new_height)

        elif (height != 0) and (width == 0):
            if height >= orig_height:
                image = image.resize((round((orig_width/orig_height)*height), orig_height))
                (new_width, new_height) = image.size
                new_width = orig_width
                print('size3',new_width, new_height)
            else:
                image = image.resize((round((orig_width/orig_height)*height), height))
                (new_width, new_height) = image.size
                print('size4',new_width, new_height)
        else:
            new_width = orig_width
            new_height = orig_height

        return render(request, 'images/detail.html', {'form': form, 'out': os.path.normpath(settings.MEDIA_URL + image_name) , 'new_height': str(new_height), 'new_width': str(new_width)})
    else:
        form = ImagesizeForm()
    return render(request, 'images/detail.html', {'form': form, 'out': os.path.normpath(settings.MEDIA_URL + image_name)})

def descr(request, img_name):
    return render(request, 'images/descr.html', {'img_name': img_name})
