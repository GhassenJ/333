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
import re
from operator import itemgetter

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

@login_required
def all_buying_posts(request):
    """
    This view returns JSON data for all postings for buying
    """
    postings = Posting.objects.all().filter(is_selling=False).filter(is_open=True).order_by('-date_posted') #List of posts that are for buying

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

@login_required
def all_selling_posts(request):
    """
    This view returns JSON data for all postings for selling
    """
    # Get all postings that are for selling
    postings = Posting.objects.all().filter(is_selling=True).filter(is_open=True).order_by('-date_posted') #List of posts that are for selling

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

@login_required
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
        category_post_list = category.posting_set.all().filter(is_selling=False).filter(is_open=True).order_by('-date_posted')
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

@login_required
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
        category_post_list = category.posting_set.all().filter(is_selling=True).filter(is_open=True).order_by('-date_posted')
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

@login_required
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
        hashtag_post_list = hashtag.posting_set.all().filter(is_selling=False).filter(is_open=True).order_by('-date_posted')
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

@login_required
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
        hashtag_post_list = hashtag.posting_set.all().filter(is_selling=True).filter(is_open=True).order_by('-date_posted')
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

@login_required
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

@login_required
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
@login_required
def search_posts(request, query):
    """
    This view gets all open posts that are relevant to the given query and returns
    the posts in a ranking order.
    Ranking order is determined 
    1) AND of all the words in the query (how many hit)
    2) hit importance from most to least (title, hashtags, category)
    3) Relevance to current user (do hashtags in post relate to hashtags of user?)
    4) date posted from newest to oldest
    5) and is case insensitive
    """

    import logging
    logger = logging.getLogger(__name__)


    user = request.user
    hashtags = user.userprofile.hashtags.all()
    categories = user.userprofile.categories.all()
    #logger.info(hashtags)
    #logger.info(categories)

    response_list=[]
    #posting_ids=[]
    post_list = Posting.objects.all().filter(is_open=True).order_by('-date_posted')
    
    query_list=query.__str__().split(' ')
    # to make this case insensitive:
    for i in range(len(query_list)):
        query_list[i] = query_list[i].lower()
        #logger.info(query_list[i])
    for posting in post_list:
        """
        search strings listed in order (from high to low) of weight given if match found
        """
        titlesearchstring = posting.title.__str__() 
        hashtagsearchstring = ""
        for i in range(len(posting.hashtags.all())):
            hashtagsearchstring += posting.hashtags.all()[i].__str__()
        descriptionsearchstring = posting.description.__str__() 
        categorysearchstring = posting.category.__str__() 
        #logger.info(hashtagsearchstring)
        #logger.info(categorysearchstring)

        Tmatches = []
        Hmatches = []
        Dmatches = []
        Cmatches = []

        titlesearchstring = titlesearchstring.lower()
        hashtagsearchstring = hashtagsearchstring.lower()
        descriptionsearchstring = descriptionsearchstring.lower()
        categorysearchstring = categorysearchstring.lower()

        for q in query_list:
            Tmatches.extend(re.findall(q, titlesearchstring))
            #logger.info(q)
            #logger.info(titlesearchstring)
            Hmatches.extend(re.findall(q, hashtagsearchstring))
            Dmatches.extend(re.findall(q, descriptionsearchstring))
            Cmatches.extend(re.findall(q, categorysearchstring))


        """
        assign weights to the matches
        """
        numMatches = 0
        titleMatches = len(Tmatches)
        hashtagMatches = len(Hmatches)
        descriptionMatches = len(Dmatches)
        categoryMatches = len(Cmatches)

        """
        if user's hashtags match posting's hashtags, increase rank factor for hashtags
        """
        hashtagFactor = 1
        categoryFactor = 1
        for h in hashtags:
            if (len(re.findall(h.name, hashtagsearchstring))>0):
                hashtagFactor = hashtagFactor + 1
        for c in categories:
            if (len(re.findall(c.name, categorysearchstring))>0):
                categoryFactor = categoryFactor + 1

        numMatches = titleMatches*4 + hashtagMatches*hashtagFactor*3 + descriptionMatches*2 + categoryMatches*categoryFactor*1
        matches = []
        matches.extend(Tmatches)
        matches.extend(Hmatches)
        matches.extend(Dmatches)
        matches.extend(Cmatches)

        #if (numMatches > 0 and posting.id not in posting_ids):
        if (numMatches > 0):
            #posting_ids.append(posting.id)
            postdata = {}
            #postdata['matches'] = matches
            postdata['numMatches'] = numMatches
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
            hashtags2 = []
            for hashtag in posting.hashtags.all():
                hashtags2.append({"name": hashtag.name, "id": hashtag.id})
            postdata['hashtags'] = hashtags2
            response_list.append(postdata)

    """
    sort by numMatches
    """
    templist = sorted(response_list, key=lambda resp: resp['numMatches'])
    templist.reverse()
    response_list = templist

    """
    Remove numMatches from response_list
    """
    for response in response_list:
        del response['numMatches']
    return HttpResponse(json.dumps(response_list), content_type="application/json")

