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
### GENERIC POSTING-BASED VIEWS:
###     -all_buying_posts(request)
###     -all_selling_posts(request)
###     -category_buying_posts(request, category_id)
###     -category_selling_posts(request, category_id)
###     -hashtag_buying_posts(request, hashtag_id)
###     -hashtag_selling_posts(request, hashtag_id)
###     -all_categories(request)
###     -all_hashtags(request)
###     -search_posts(request)
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

##################################################################################
### GETTING RELEVANT POSTS FROM QUERY IN SEARCH     
##################################################################################

def search_posts(request, query):
    """
    This view gets all open posts that are relevant to the given query and returns
    the posts in a ranking order.
    Ranking order is determined 
    1) AND of all the words in the query (how many hit)
    2) hit importance from most to least (title, hashtags, category)
    3) date posted from newest to oldest
    """

    response_list=[]
    posting_ids=[]
    post_list = Posting.objects.all().filter(is_open=True).order_by('date_posted').reverse()
    query_list=query.split(' ')
    for posting in post_list:
        """

        """
        searchstring = posting.title + posting.description + posting.category + posting.hashtags
        matches = []
        for q in query_list:
            matches.append(re.findall(q, searchstring))
        if (len(matches) > 0 and posting.id not in posting_ids):
            posting_ids.append(posting.id)
            postdata = {}
            postdata['numMatches'] = len(matches)
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
            postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
            postdata['id'] = posting.id
            postdata['image'] = posting.picture
            hashtags = []
            for hashtag in posting.hashtags.all():
                hashtags.append({"name": hashtag.name, "id": hashtag.id})
            postdata['hashtags'] = hashtags
            response_list.append(postdata)

    """
    sort by numMatches
    """
    response_list.order_by('numMatches')

    """
    Remove numMatches from response_list
    """
    for response in response_list:
        del response['numMatches']
    return HttpResponse(json.dumps(response_list), content_type="application/json")

