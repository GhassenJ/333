from django import forms
from market.models import *
from django.contrib.auth.models import User
from parsley.decorators import parsleyfy
# Forms for postings

# Form for creating a new posting
@parsleyfy
class PostingForm(forms.ModelForm):
    hashtags = forms.CharField(max_length = 200)
    is_selling = forms.BooleanField(label='Selling?', required = False, initial=False)
    class Meta:
        model = Posting
        fields = ('title', 'is_selling', 'category', 'date_expires', 'price', 'method_of_pay', 'description', 'picture')

# Form for editing a posting
class PostingEditForm(forms.ModelForm):
    is_selling = forms.BooleanField(label='Selling?', required = False, initial=False)
    class Meta:
        model = Posting
        fields = ('title', 'is_selling', 'category', 'date_expires', 'price', 'method_of_pay', 'description', 'picture')

# Form for creating a new user
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

# Form for creating a new user profile
class UserProfileForm(forms.ModelForm):
    categories = forms.widgets.CheckboxSelectMultiple()
    categories.help_text = ""
    categories.queryset = Category.objects.all()
    class Meta:
        model = UserProfile
        fields = ('phone_no', 'class_year', 'categories')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_no', 'class_year', 'categories', 'hashtags')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'description', 'rating')


