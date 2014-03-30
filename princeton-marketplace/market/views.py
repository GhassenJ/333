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
### HOMEPAGE (TEMPORARY)
######################################################################################
def display_postings(request):
    """
    This view displays either all postings (for a non-authenticated user), or
    postings from subscribed categories, from my posting set, and from my replied set.
    """
    # Get the currently-signed-in user
    user = request.user

    #If the user is authenticated, then display categories
    if user.is_authenticated():
        my_author_list = user.author.all().order_by('date_posted') #List of posts I've authored
        my_respond_list = user.responder.all().order_by('date_posted') #List of posts I've responded to
        full_posting_list = Posting.objects.all().filter(is_open=True).order_by('date_posted') #List of all posts
        posting_list = {} #List of posts in my subscribed categories

        # Build list from subscribed categories
        for category in user.userprofile.categories.all():
            posting_list[category.name] = full_posting_list.filter(category = category)

        context = {'posting_list': posting_list, 'my_author_list': my_author_list, 'my_respond_list': my_respond_list}
        return render(request, 'market/index.html', context)

    # Otherwise, display every post.
    else:
        full_posting_list = Posting.objects.all().filter(is_open=True).order_by('date_posted')
        posting_list = {}

        # Build list from all categories
        for category in Category.objects.all():
            posting_list[category.name] = full_posting_list.filter(category = category)
        context = {'posting_list': posting_list}
        return render(request, 'market/index.html', context)

@login_required
def create_posting(request):
    """
    This view allows an authed user to create a new posting.
    """

    # If we're doing a POST, read in form data and save it
    if request.method == 'POST':
        form = PostingForm(data=request.POST)

        # Process a valid form:
        if form.is_valid():
            # Save information from the PostingForm
            posting = form.save(commit=False)

            # Save additional information (author, is_open, date_posted)
            posting.author = request.user
            posting.is_open = True
            posting.date_posted = timezone.now()

            # Save the M2M fields (hashtag and category)
            posting.save()
            form.save_m2m()


            if request.is_ajax():
                return HttpResponse('OK')
            else:
                return HttpResponseRedirect(reverse('market:index', args=''))
        # Return Errors
        else:
            if request.is_ajax():
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)
                return HttpResponseBadRequest(json.dumps(errors_dict))
            else:
                print form.errors

    # Otherwise, post the empty form for the user to fill in.
    else:
        form = PostingForm()

    return render(request, 'market/create_posting.html', {'form': form})

@login_required
def delete_posting(request, posting_id):
    """
    This method allows a user to delete a posting (specified by posting_id)
    """
    # Ensure that the posting exists
    try:
        posting = Posting.objects.get(pk=posting_id)
    except Posting.DoesNotExist:
        raise Http404
    else:

        user = request.user
        if request.method == 'POST':
            # Only delete if the currently-logged user authored the post.
            if user == posting.author:
                posting.delete()
                if request.is_ajax():
                    return HttpReponse('OK')
                else:
                    return HttpResponseRedirect(reverse('market:index', args=''))
            else:
                raise Http404
        # Redirect to homepage
        return HttpResponseRedirect(reverse('market:index', args='')) 

@login_required
def close_posting(request, posting_id):
    """
    Close a posting, updating the transaction count for both the user and the responder
    """
    try:
        posting = Posting.objects.get(pk=posting_id)
    except Posting.DoesNotExist:
        raise Http404
    else:
        user = request.user
        if user != posting.author:
            raise Http404
        if posting.responder is None:
            raise Http404
        if request.method == 'POST':
            user.userprofile.transactions = user.userprofile.transactions + 1
            posting.responder.userprofile.transactions = posting.responder.userprofile.transactions + 1
            posting.delete()
            if request.is_ajax():
                return HttpResponse('OK')
            else:
                return HttpResponseRedirect(reverse('market:index', args=''))
        return HttpResponseRedirect(reverse('market:index', args='')) 

@login_required
def respond_to_posting(request, posting_id):
    """
    This method allows a user to respond to a posting (specified by posting_id)
    """

    #Ensure that the posting exists
    try:
        posting = Posting.objects.get(pk=posting_id)
    except Posting.DoesNotExist:
        raise Http404
    else:
        user = request.user
        if request.method == 'POST':

            posting.is_open = False;
            posting.responder = user;
            posting.save()
            if request.is_ajax():
                return HttpReponse('OK')
            else:
                return HttpResponseRedirect(reverse('market:index', args=''))

        # Redirect to homepage
        return HttpResponseRedirect(reverse('market:index', args='')) 


@login_required
def remove_responder(request, posting_id):
    """
    This method allows a user to respond to a posting (specified by posting_id)
    """

    #Ensure that the posting exists
    try:
        posting = Posting.objects.get(pk=posting_id)
    except Posting.DoesNotExist:
        raise Http404
    else:
        user = request.user
        if request.method == 'POST':
            if request.user == posting.author:
                posting.is_open = True;
                posting.responder = "";
                posting.save()
                if request.is_ajax():
                    return HttpReponse('OK')
                else:
                    return HttpResponseRedirect(reverse('market:index', args=''))

        # Redirect to homepage
        return HttpResponseRedirect(reverse('market:index', args='')) 


@login_required
def edit_profile(request):
    """
    Allows a user to edit their profile information
    """

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

    return render(request, 'market/edit_profile.html',  {'user_form': user_form, 'user_profile_form': user_profile_form})
    #return render_to_response('market/create_posting.html', {'form': form}, context)


@login_required
def edit_posting(request, posting_id):
    """
    """

    try: # validate posting_id
        posting = Posting.objects.get(pk=posting_id)
    except Posting.DoesNotExist:
        raise Http404
    else:
        # If we're doing a POST, read in form data and save it
        if request.method == 'POST': 
            if request.user == posting.author:
                posting_form = PostingEditForm(data=request.POST)


                if posting_form.is_valid():
                    posting_form = PostingEditForm(request.POST, instance=posting)
                    tempposting = posting_form.save(commit=False)
                    tempposting.save()
                    posting_form.save_m2m()

                    if request.is_ajax():
                        return HttpResponse('OK')
                    else:
                        return HttpResponseRedirect(reverse('market:index', args=''))
                else:
                    if request.is_ajax():
                        errors_dict = {}
                        if posting_form.errors:
                            for error in posting_form.errors:
                                e = posting_form.errors[error]
                                errors_dict[error] = unicode(e)
                        return HttpResponseBadRequest(json.dumps(errors_dict))
                    else:
                        print posting_form.errors
            else:
                raise Http404

        # Otherwise, post the empty form for the user to fill in.
        else:
            if request.user == posting.author:
                posting_form = PostingEditForm(instance=posting)
            else:
                raise Http404

        return render(request, 'market/edit_posting.html',  {'posting_form': posting_form, 'posting_id': posting.id})



######################################################################################
### USER ACCOUNT MANAGEMENT FUNCTIONS (TEMPORARY)
######################################################################################

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
            user = user_form.save()
            user.set_password(user.password)
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
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('market/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    """
    This view allows a user to login.
    """
    context = RequestContext(request)

    # If a POST, fill in required user data and authenticate
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # Login good, proceed back to home page
            login(request, user)
            return HttpResponseRedirect(reverse('market:index', args=''))
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # Display the form (note: this form is stuck in the template)
    else:
        return render_to_response('market/login.html', {}, context)

@login_required
def user_logout(request):
    """
    Logs the current user out.
    """
    # Logout the user
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('market:index', args=''))

######################################################################################
### PERSONALIZED POST (GET) VIEWS
######################################################################################

@login_required
def my_open_posts(request):
    """
    This view returns JSON data for all postings created by the current user
    that are open. Ordered by date.
    """
    # Get the currently-signed-in user
    user = request.user

    #If the user is authenticated, then display categories
    if user.is_authenticated():
        my_author_list = user.author.all().filter(is_open=True).order_by('date_posted') #List of posts I've authored
        response_list = []
        for posting in my_author_list:
            postdata = {}
            postdata['title'] = posting.title
            postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
            postdata['date_posted'] = posting.date_posted.__str__()
            postdata['date_expires'] = posting.date_expires.__str__()
            postdata['method_of_payment'] = posting.method_of_pay
            postdata['price'] = posting.price
            postdata['description'] = posting.description
            postdata['is_selling'] = posting.is_selling
            postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
            postdata['id'] = posting.id
            postdata['image'] = posting.picture
            hashtags = []
            for hashtag in posting.hashtags.all():
                hashtags.append({"name": hashtag.name, "id": hashtag.id})
            postdata['hashtags'] = hashtags
            response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")

@login_required
def my_closed_posts(request):
    """
    This view returns JSON data for all postings created by the current user 
    that was responded to. Ordered by date.
    """
    # Get the currently-signed-in user
    user = request.user

    #If the user is authenticated, then display categories
    if user.is_authenticated():
        my_author_list = user.author.all().filter(is_open=False).order_by('date_posted') #List of posts I've authored that are closed
        response_list = []
        for posting in my_author_list:
            postdata = {}
            postdata['title'] = posting.title
            postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
            postdata['responder'] = {"username":posting.responder.username, "id":posting.responder.id}
            postdata['date_posted'] = posting.date_posted.__str__()
            postdata['date_expires'] = posting.date_expires.__str__()
            postdata['method_of_payment'] = posting.method_of_pay
            postdata['price'] = posting.price
            postdata['description'] = posting.description
            postdata['is_selling'] = posting.is_selling
            postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
            postdata['id'] = posting.id
            postdata['image'] = posting.picture
            hashtags = []
            for hashtag in posting.hashtags.all():
                hashtags.append({"name": hashtag.name, "id": hashtag.id})
            postdata['hashtags'] = hashtags
            response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")


@login_required
def my_responded_posts(request):
    """
    This view returns JSON data for all postings that the logged user 
    has responded to.
    """
    # Get the currently-signed-in user
    user = request.user

    #If the user is authenticated, then display categories
    if user.is_authenticated():
        my_responded_list = user.responder.all().order_by('date_posted') #List of posts I've authored
        response_list = []
        for posting in my_responded_list:
            postdata = {}
            postdata['title'] = posting.title
            postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
            postdata['responder'] = {"username":posting.responder.username, "id":posting.responder.id}
            postdata['date_posted'] = posting.date_posted.__str__()
            postdata['date_expires'] = posting.date_expires.__str__()
            postdata['method_of_payment'] = posting.method_of_pay
            postdata['price'] = posting.price
            postdata['description'] = posting.description
            postdata['is_selling'] = posting.is_selling
            postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
            postdata['id'] = posting.id
            postdata['image'] = posting.picture
            hashtags = []
            for hashtag in posting.hashtags.all():
                hashtags.append({"name": hashtag.name, "id": hashtag.id})
            postdata['hashtags'] = hashtags
            response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")


######################################################################################
### GENERIC POST (GET) VIEWS
######################################################################################

def all_buying_posts(request):
    """
    This view returns JSON data for all postings for buying
    """
    # Get all postings that are for buying
    postings = Posting.objects.all().filter(is_selling=False).order_by('date_posted') #List of posts that are for buying

    # For all postings that are for buying
    response_list = []
    for posting in postings:
        postdata = {}
        postdata['title'] = posting.title
        postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
        if (posting.responder is not None):
            postdata['responder'] = {"username":posting.responder.username, "id":posting.responder.id}
        else:
            postdata['responder'] = {}
        postdata['date_posted'] = posting.date_posted.__str__()
        postdata['date_expires'] = posting.date_expires.__str__()
        postdata['method_of_payment'] = posting.method_of_pay
        postdata['price'] = posting.price
        postdata['description'] = posting.description
        postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
        postdata['id'] = posting.id
        postdata['image'] = posting.picture
        hashtags = []
        for hashtag in posting.hashtags.all():
            hashtags.append({"name": hashtag.name, "id": hashtag.id})
        postdata['hashtags'] = hashtags
        response_list.append(postdata)
    return HttpResponse(json.dumps(response_list), content_type="application/json")

def all_selling_posts(request):
    """
    This view returns JSON data for all postings for selling
    """
    # Get all postings that are for selling
    postings = Posting.objects.all().filter(is_selling=True).order_by('date_posted') #List of posts that are for selling

    #For all postings that are for selling
    response_list = []
    for posting in postings:
        postdata = {}
        postdata['title'] = posting.title
        postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
        if (posting.responder is not None):
            postdata['responder'] = {"username":posting.responder.username, "id":posting.responder.id}
        else:
            postdata['responder'] = {}
        postdata['date_posted'] = posting.date_posted.__str__()
        postdata['date_expires'] = posting.date_expires.__str__()
        postdata['method_of_payment'] = posting.method_of_pay
        postdata['price'] = posting.price
        postdata['description'] = posting.description
        postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
        postdata['id'] = posting.id
        postdata['image'] = posting.picture
        hashtags = []
        for hashtag in posting.hashtags.all():
            hashtags.append({"name": hashtag.name, "id": hashtag.id})
        postdata['hashtags'] = hashtags
        response_list.append(postdata)
    return HttpResponse(json.dumps(response_list), content_type="application/json")

######################################################################################
### GETTING VIEWS FOR CATEGORIES AND HASHTAGS
######################################################################################

def all_categories(request):
    """
    This view returns JSON data for all categories
    """
    # Get all categories
    categories = Category.objects.all().order_by('name')
    response_list = []
    for category in categories:
        postdata = {}
        postdata['name'] = category.name
        postdata['number'] = category.num_posts
        postdata['id'] = category.id
        response_list.append(postdata)
    return HttpResponse(json.dumps(response_list), content_type="application/json")

def all_hashtags(request):
    """
    This view returns JSON data for all hashtags
    """
    # Get all categories
    hashtags = Hashtag.objects.all().order_by('name')
    response_list = []
    for hashtag in hashtags:
        postdata = {}
        postdata['name'] = hashtag.name
        postdata['frequency'] = hashtag.frequency
        postdata['id'] = hashtag.id
        response_list.append(postdata)
    return HttpResponse(json.dumps(response_list), content_type="application/json")

######################################################################################
### POST-GETTING VIEWS FOR CATEGORIES AND HASHTAGS
######################################################################################

def category_buying_posts(request, category_id):
    """
    This view gets all buying posts under the category identified by category_id
    """
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404
    else:
        response_list=[]
        category_post_list = category.posting_set.all().filter(is_selling=False).order_by('date_posted')
        for posting in category_post_list:
            postdata = {}
            postdata['title'] = posting.title
            postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
            if (posting.responder is not None):
                postdata['responder'] = {"username":posting.responder.username, "id":posting.responder.id}
            else:
                postdata['responder'] = {}
            postdata['date_posted'] = posting.date_posted.__str__()
            postdata['date_expires'] = posting.date_expires.__str__()
            postdata['method_of_payment'] = posting.method_of_pay
            postdata['price'] = posting.price
            postdata['description'] = posting.description
            postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
            postdata['id'] = posting.id
            postdata['image'] = posting.picture
            hashtags = []
            for hashtag in posting.hashtags.all():
                hashtags.append({"name": hashtag.name, "id": hashtag.id})
            postdata['hashtags'] = hashtags
            response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")

def category_selling_posts(request, category_id):
    """
    This view gets all selling posts under the category identified by category_id
    """
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404
    else:
        response_list=[]
        category_post_list = category.posting_set.all().filter(is_selling=True).order_by('date_posted')
        for posting in category_post_list:
            postdata = {}
            postdata['title'] = posting.title
            postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
            if (posting.responder is not None):
                postdata['responder'] = {"username":posting.responder.username, "id":posting.responder.id}
            else:
                postdata['responder'] = {}
            postdata['date_posted'] = posting.date_posted.__str__()
            postdata['date_expires'] = posting.date_expires.__str__()
            postdata['method_of_payment'] = posting.method_of_pay
            postdata['price'] = posting.price
            postdata['description'] = posting.description
            postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
            postdata['id'] = posting.id
            postdata['image'] = posting.picture
            hashtags = []
            for hashtag in posting.hashtags.all():
                hashtags.append({"name": hashtag.name, "id": hashtag.id})
            postdata['hashtags'] = hashtags
            response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")

def hashtag_buying_posts(request, hashtag_id):
    """
    This view gets all buying posts under the hashtag identified by hashtag_id
    """
    try:
        hashtag = Hashtag.objects.get(pk=hashtag_id)
    except Hashtag.DoesNotExist:
        raise Http404
    else:
        response_list=[]
        hashtag_post_list = hashtag.posting_set.all().filter(is_selling=False).order_by('date_posted')
        for posting in hashtag_post_list:
            postdata = {}
            postdata['title'] = posting.title
            postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
            if (posting.responder is not None):
                postdata['responder'] = {"username":posting.responder.username, "id":posting.responder.id}
            else:
                postdata['responder'] = {}
            postdata['date_posted'] = posting.date_posted.__str__()
            postdata['date_expires'] = posting.date_expires.__str__()
            postdata['method_of_payment'] = posting.method_of_pay
            postdata['price'] = posting.price
            postdata['description'] = posting.description
            postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
            postdata['id'] = posting.id
            postdata['image'] = posting.picture
            hashtags = []
            for hashtag in posting.hashtags.all():
                hashtags.append({"name": hashtag.name, "id": hashtag.id})
            postdata['hashtags'] = hashtags
            response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")

def hashtag_selling_posts(request, hashtag_id):
    """
    This view gets all selling posts under the hashtag identified by hashtag_id
    """
    try:
        hashtag = Hashtag.objects.get(pk=hashtag_id)
    except Hashtag.DoesNotExist:
        raise Http404
    else:
        response_list=[]
        hashtag_post_list = hashtag.posting_set.all().filter(is_selling=True).order_by('date_posted')
        for posting in hashtag_post_list:
            postdata = {}
            postdata['title'] = posting.title
            postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
            if (posting.responder is not None):
                postdata['responder'] = {"username":posting.responder.username, "id":posting.responder.id}
            else:
                postdata['responder'] = {}
            postdata['date_posted'] = posting.date_posted.__str__()
            postdata['date_expires'] = posting.date_expires.__str__()
            postdata['method_of_payment'] = posting.method_of_pay
            postdata['price'] = posting.price
            postdata['description'] = posting.description
            postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
            postdata['id'] = posting.id
            postdata['image'] = posting.picture
            hashtags = []
            for hashtag in posting.hashtags.all():
                hashtags.append({"name": hashtag.name, "id": hashtag.id})
            postdata['hashtags'] = hashtags
            response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")

######################################################################################
### GETTER FOR A USER'S REVIEWS
######################################################################################

def get_reviews(request, user_id):
    """
    This view gets the reviews for the user whose id is user_id
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404
    else: 
        review_list = user.review_reviewee.all().order_by('date_posted') #List of posts I've authored that are closed
        response_list = []
        for review in review_list:
            postdata = {}
            postdata['title'] = review.title
            postdata['rating'] = review.rating
            postdata['id'] = review.id
            response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")

######################################################################################
### DETAIL FETCHING VIEWS FOR POSTINGS, USERS, AND REVIEWS
######################################################################################

def review_detail(request, review_id):
    """
    This view gets the reviews for the user
    """
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        raise Http404
    else: 

    #If the user is authenticated, then display categories
        response_list = []
        postdata = {}
        reviewer = {}
        reviewee = {}
        postdata['title'] = review.title
        postdata['description'] = review.description
        postdata['date'] = review.date_posted.__str__()
        postdata['rating'] = review.rating
        reviewer['username'] = review.author.username
        reviewer['id'] = review.author.id
        reviewee['username'] = review.reviewee.username
        reviewee['id'] = review.reviewee.id
        postdata['reviewer'] = reviewer
        postdata['reviewee'] = reviewee
        postdata['id'] = review.id
        response_list.append(postdata)
        return HttpResponse(json.dumps(response_list), content_type="application/json")

def posting_detail(request, posting_id):
    """
    This view gets the details of a posting whose id is posting_id
    """
    try:
        posting = Posting.objects.get(pk=posting_id)
    except Posting.DoesNotExist:
        raise Http404
    else: 
        postdata = {}
        postdata['title'] = posting.title
        postdata['author'] = {"username":posting.author.username, "id":posting.author.id}
        if (posting.responder is not None):
            postdata['responder'] = {"username":posting.responder.username, "id":posting.responder.id}
        else:
            postdata['responder'] = {}
        postdata['date_posted'] = posting.date_posted.__str__()
        postdata['date_expires'] = posting.date_expires.__str__()
        postdata['method_of_payment'] = posting.method_of_pay
        postdata['price'] = posting.price
        postdata['description'] = posting.description
        postdata['selling'] = posting.is_selling
        postdata['open'] = posting.is_open
        postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
        postdata['id'] = posting.id
        postdata['image'] = posting.picture
        hashtags = []
        for hashtag in posting.hashtags.all():
            hashtags.append({"name": hashtag.name, "id": hashtag.id})
        postdata['hashtags'] = hashtags
        return HttpResponse(json.dumps(postdata), content_type="application/json")


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

