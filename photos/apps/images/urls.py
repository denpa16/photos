from django.urls import path

from . import views
app_name = 'images'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('add/', views.add_photo, name = 'add_photo'),
    path('<image_name>/', views.detail, name = 'detail')
    
]