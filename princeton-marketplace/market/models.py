from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.

# Control-defined categories for goods and services
class Category(models.Model):
    name = models.CharField(max_length = 200)
    num_posts = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.name

# Hashtag categorization
class Hashtag(models.Model):
    name = models.CharField(max_length = 200)
    frequency = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.name

# A profile for each user
class UserProfile(models.Model):
    user = models.OneToOneField(User) # Link to authenticated user object
    phone_no = models.CharField(max_length = 20)
    class_year = models.IntegerField(default = 2000)
    categories = models.ManyToManyField(Category) # Link to desired categories
    hashtags = models.ManyToManyField(Hashtag, blank=True, null=True) # Link to hashtags used
    rating = models.IntegerField(default = 0)
    transactions = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.user.username

# User Reviews
class Review(models.Model):
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 4000)
    date_posted = models.DateTimeField('Date Posted', default = timezone.now())
    rating = models.IntegerField(default = 5)
    author = models.ForeignKey(User, related_name='review_author')
    reviewee = models.ForeignKey(User, related_name='review_reviewee')

# A buying or selling post
class Posting(models.Model):
    title = models.CharField(max_length = 200)
    
    author = models.ForeignKey(User, related_name='author') # Link to user author
    responder = models.ForeignKey(User, related_name='responder', blank=True, null=True) # Link to user responder
    
    date_posted = models.DateTimeField('Date Posted', default = timezone.now())
    date_expires = models.DateTimeField('Expiration Date', default = timezone.now())
    
    method_of_pay = models.CharField(max_length = 200)
    price = models.CharField(max_length = 50)

    description = models.CharField(max_length = 2000)
    
    is_selling = models.BooleanField(default = True)
    is_open = models.BooleanField(default = True)

    category = models.ForeignKey(Category) # Link to relevant category
    hashtags = models.ManyToManyField(Hashtag, blank=True, null=True)

    picture = models.ImageField(upload_to='post_images', blank=True)
    def __unicode__(self):
        return self.title