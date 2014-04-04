from review_views import *
######################################################################################
### REVIEW-BASED VIEWS:
###     -review_detail(request, review_id)
###     -write_review(request, review_id)
######################################################################################

from user_views import *
######################################################################################
### USER-ACCOUNT-BASED VIEWS:
###     -register(request)
###     -user_login(request)
###     -user_logout(request)
###     -user_detail(request, user_id)
###     -edit_profile(request)
###     -get_reviews(request, user_id)
######################################################################################

from generic_post_views import *
######################################################################################
### GENERIC POSTING-BASED VIEWS:
###     -all_buying_posts(request)
###     -all_selling_posts(request)
###     -category_buying_posts(request, category_id)
###     -category_selling_posts(request, category_id)
###     -hashtag_buying_posts(request, hashtag_id)
###     -hashtag_selling_posts(request, hashtag_id)
###     -all_categories(request)
###     -all_hashtags(request)
######################################################################################

from personal_post_views import *
######################################################################################
### PERSONAL POSTING-BASED VIEWS:
###     -my_open_posts(request)
###     -my_closed_posts(request)
###     -my_responded_posts(request)
######################################################################################

from posting_views import *
######################################################################################
### POSTING MANAGEMENT VIEWS
###     -create_posting(request)
###     -delete_posting(request, posting_id)
###     -close_posting(request, posting_id)
###     -respond_to_posting(request, posting_id)
###     -remove_responder(request, posting_id)
###     -edit_posting(request, posting_id)
###     -posting_detail(request, posting_id)
######################################################################################



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
        try: 
            test = user.userprofile
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect(reverse('market:register', args=''))
        else:
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