from django import forms
from market.models import *
from django.contrib.auth.models import User

# Forms for postings

# Form for creating a new posting
class PostingForm(forms.ModelForm):
    is_selling = forms.BooleanField(label='Buying?', required = False, initial=False)
    class Meta:
        model = Posting
        fields = ('title', 'is_selling', 'category', 'date_expires', 'price', 'method_of_pay', 'description')

# Form for creating a new user
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

# Form for creating a new user profile
class UserProfileForm(forms.ModelForm):
    categories = forms.widgets.CheckboxSelectMultiple()
    categories.help_text = ""
    categories.queryset = Category.objects.all()
    class Meta:
        model = UserProfile
        fields = ('phone_no', 'class_year', 'categories')