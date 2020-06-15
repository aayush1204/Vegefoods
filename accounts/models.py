

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone


class Signup(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    address = models.TextField()
    number = models.CharField(max_length=15)
    username =models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    #data_created=models.DateTimeField(auto_now_add=True)
#    def publish_blog(self):
#        self.published_date = timezone.now()
#        self.save()

    def __str__(self):
        return self.name