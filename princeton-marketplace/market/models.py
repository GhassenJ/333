from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.

# Control-defined categories for goods and services
class Category(models.Model):
    name = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.name

# A profile for each user
class UserProfile(models.Model):
    user = models.OneToOneField(User) # Link to authenticated user object
    phone_no = models.CharField(max_length = 20)
    class_year = models.IntegerField(default = 2000)
    categories = models.ManyToManyField(Category) # Link to desired categories
    transactions = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.user.username

# A buying or selling post
class Posting(models.Model):
    title = models.CharField(max_length = 200)
    author = models.ForeignKey(User, related_name='author') # Link to user author
    is_open = models.BooleanField(default = True)
    responder = models.ManyToManyField(User, related_name='responder') # Link to user responders
    date_posted = models.DateTimeField('Date Posted', default = timezone.now())
    date_expires = models.DateTimeField('Expiration Date', default = timezone.now())
    method_of_pay = models.CharField(max_length = 200)
    category = models.ForeignKey(Category) # Link to relevant category
    description = models.CharField(max_length = 2000)
    price = models.CharField(max_length = 50)
    is_selling = models.BooleanField(default = True)
    def __unicode__(self):
        return self.title