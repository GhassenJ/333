from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.name

class User(models.Model):
    netid = models.CharField(max_length = 20)
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    phone_no = models.CharField(max_length = 20)
    class_year = models.IntegerField(default = 2000)
    categories = models.ManyToManyField(Category)
    transactions = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.name

class Posting(models.Model):
    title = models.CharField(max_length = 200)
    author = models.ForeignKey(User, related_name='author')
    is_open = models.BooleanField(default = True)
    responder = models.ManyToManyField(User, related_name='responder')
    date_posted = models.DateTimeField('Date Posted')
    date_expires = models.DateTimeField('Expiration Date')
    method_of_pay = models.CharField(max_length = 200)
    category = models.ForeignKey(Category)
    description = models.CharField(max_length = 2000)
    price = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.title
