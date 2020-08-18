from django.db import models


class Image(models.Model):
    image = models.ImageField(blank = True)
    title = models.CharField(max_length = 200, blank = True)
    url = models.URLField(blank = True)

    def __str__(self):
        return self.title

class Imagesize(models.Model):
    height =  models.CharField(max_length=50, blank = True)
    width =  models.CharField(max_length=50, blank = True)


