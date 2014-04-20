from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
from market.models import *
from market.forms import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

######################################################################################
### USER-ACCOUNT-BASED VIEWS:
###     -register(request)
###     -user_login(request)
###     -user_logout(request)
###     -user_detail(request, user_id)
###     -edit_profile(request)
###     -get_reviews(request, user_id)
######################################################################################

@login_required
def register(request):
    """
    This view allows a new user to create an account.
    """
    context = RequestContext(request)

    # Have we registered yet?
    registered = False

    # If a POST, fill in required user data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            new_form = UserForm(request.POST, instance=request.user)
            user = new_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            profile_form.save_m2m()
            registered = True
        
        else:
            print user_form.errors, profile_form.errors

    # Otherwise, send up forms for filling
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm()

    return render_to_response('market/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_detail(request, user_id):
    """
    This view gets the details of a user whose id is user_id.
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404
    else: 
        userprofile = user.userprofile
        userdata = {}
        userdata["username"] = user.username
        userdata["firstname"] = user.first_name
        userdata["lastname"] = user.last_name
        userdata["email"] = user.email
        userdata["phone"] = userprofile.phone_no
        userdata["year"] = userprofile.class_year
        userdata["rating"] = userprofile.rating
        userdata["transactions"] = userprofile.transactions
        categories = []
        for category in userprofile.categories.all():
            categories.append({"name": category.name, "id": category.id})
        userdata["categories"] = categories
        hashtags = []
        for hashtag in userprofile.hashtags.all():
            hashtags.append({"name": hashtag.name, "id": hashtag.id})
        userdata["hashtags"] = hashtags
        reviews = []
        for review in user.review_reviewee.all():
            reviews.append({"title": review.title, "rating": review.rating, "id": review.id})
        userdata["reviews"] = reviews
        userdata["id"] = user.id
        return HttpResponse(json.dumps(userdata), content_type="application/json")

@login_required
def edit_profile(request):
    """
    Allows a user to edit their profile information
    """

    template = ''
    if (request.is_ajax()):
        template = 'market/edit_profile_form.html'
    else:
        template = 'market/edit_profile.html'

    # If we're doing a POST, read in form data and save it
    if request.method == 'POST':
        # Load the User and UserProfile forms
        user_form = UserEditForm(data=request.POST)
        user_profile_form = UserProfileEditForm(data=request.POST)


        if user_form.is_valid() and user_profile_form.is_valid():
            # Save data for the User
            user_form = UserEditForm(request.POST, instance=request.user)
            user = user_form.save()
            user.save()

            # Save data for the UserProfile, being careful with M2M fields
            user_profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
            profile = user_profile_form.save(commit=False)
            profile.save()
            user_profile_form.save_m2m()

            if request.is_ajax():
                return HttpResponse('OK')
            else:
                return HttpResponseRedirect(reverse('market:index', args=''))
        # Return Errors as necessary.
        else:
            if request.is_ajax():
                errors_dict = {}
                if user_form.errors:
                    for error in user_form.errors:
                        e = user_form.errors[error]
                        errors_dict[error] = unicode(e)
                if user_profile_form.errors:
                    for error in user_profile_form.errors:
                        e = user_profile_form.errors[error]
                        errors_dict[error] = unicode(e)
                return HttpResponseBadRequest(json.dumps(errors_dict))
            else:
                print user_form.errors, user_profile_form.errors

    # Otherwise, post the empty form for the user to fill in.
    else:
        user_form = UserEditForm(instance=request.user)
        user_profile_form = UserProfileEditForm(instance=request.user.userprofile)

    return render(request, template,  {'user_form': user_form, 'user_profile_form': user_profile_form})
    #return render_to_response('market/create_posting.html', {'form': form}, context)

def get_reviews(request, user_id):
    """
    This view gets the reviews for the user whose id is user_id
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404
    else: 
        review_list = user.review_reviewee.all().order_by('-date_posted') #List of posts I've authored that are closed
        response_list = []
        for review in review_list:
            postdata = {}
            postdata['title'] = review.title
            postdata['rating'] = review.rating
            postdata['id'] = review.id
            response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")
