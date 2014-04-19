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
import logging
import re
logger = logging.getLogger(__name__)
#from filetransfers.api import prepare_upload, serve_file
from market.storage import prepare_upload
from google.appengine.ext.blobstore import *
import urllib
from google.appengine.api.images import *

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


@login_required
def download_handler(request, pk):
    posting = get_object_or_404(Posting, pk=pk)
    if (posting.blobstore_key != ''):
        return HttpResponse(get_serving_url(posting.blobstore_key))
    else:
        return HttpResponse("ERROR")

@login_required
def create_posting(request):
    """
    This view allows an authed user to create a new posting.
    """
    template = ''
    if (request.is_ajax()):
        template = 'market/create_posting_form.html'
    else:
        template = 'market/create_posting.html'
    # If we're doing a POST, read in form data and save it
    if request.method == 'POST':
        form = PostingForm(request.POST)
        # Process a valid form:
        if form.is_valid():
            # Save information from the PostingForm
            hashtagStr = form.cleaned_data['hashtags']
            for key, value in request.FILES.iteritems():
                logger.info(key)
            blob_key = ''
            if request.FILES.has_key('picture'):
                logger.info(request.FILES['picture'])
                blob_key = request.FILES["picture"].blobstore_info._BlobInfo__key
            hashtags = re.findall('#\w+', hashtagStr)
            hashtagsList = []
            for tag in hashtags:
                tagname = tag[1:].lower()
                logger.info(tagname)
                if (len(Hashtag.objects.all().filter(name=tagname)) != 0):
                    curtag = Hashtag.objects.get(name=tagname)
                    hashtagsList.append(curtag)
                    curtag.frequency = curtag.frequency + 1
                    curtag.save()
                else:
                    h = Hashtag(name = tagname, frequency=1)
                    h.save()
                    hashtagsList.append(h)

            posting = form.save(commit=False)

            # Save additional information (author, is_open, date_posted)
            posting.author = request.user
            posting.is_open = True
            posting.date_posted = timezone.now()
            posting.blobstore_key = blob_key;

            
            # Save the M2M fields (hashtag and category)
            posting.save()
            form.save_m2m()
            form.save()

            for hashtag in hashtagsList:
                posting.hashtags.add(hashtag)
                posting.save()
                request.user.userprofile.hashtags.add(hashtag)
                request.user.userprofile.save()

            # Update the category counts
            posting.category.num_posts = posting.category.num_posts + 1;
            posting.category.save()

            if request.is_ajax():
                #return HttpResponseRedirect('/create_posting')
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
        upload_url, upload_data = prepare_upload(request, '/create_posting/')
        form = PostingForm()

    return render(request, template, {'form': form, 'upload_url': upload_url, 'upload_data': upload_data})

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
                posting.category.num_posts = posting.category.num_posts - 1
                for i in range(len(posting.hashtags.all())):
                    posting.hashtags.all()[i].frequency = posting.hashtags.all()[i].frequency - 1
                    posting.hashtags.all()[i].save()
                posting.category.save()

                # Delete any pics associated w/ this posting
                if posting.blobstore_key != "":
                    key = BlobKey(posting.blobstore_key)
                    info = BlobInfo.get(key)
                    info.delete()
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
            user.userprofile.save()
            posting.responder.userprofile.transactions = posting.responder.userprofile.transactions + 1
            posting.responder.userprofile.save()
            if posting.blobstore_key != "":
                    key = BlobKey(posting.blobstore_key)
                    info = BlobInfo.get(key)
                    info.delete()
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
            posting.category.num_posts = posting.category.num_posts - 1;
            posting.category.save()
            hashtags = posting.hashtags.all()
            for hashtag in hashtags:
                user.userprofile.hashtags.add(hashtag)
                user.userprofile.save()

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
                posting.responder = None;
                posting.save()
                posting.category.num_posts = posting.category.num_posts + 1;
                posting.category.save()
                if request.is_ajax():
                    return HttpReponse('OK')
                else:
                    return HttpResponseRedirect(reverse('market:index', args=''))
            else:
                raise Http404
        # Redirect to homepage
        return HttpResponseRedirect(reverse('market:index', args='')) 


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
                    posting.category.num_posts = posting.category.num_posts - 1;
                    posting.category.save()
                    posting_form = PostingEditForm(request.POST, instance=posting)
                    tempposting = posting_form.save(commit=False)
                    tempposting.save()
                    posting_form.save_m2m()
                    tempposting.category.num_posts = posting.category.num_posts + 1;
                    tempposting.category.save()

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
        #postdata['image'] = posting.picture
        hashtags = []
        for hashtag in posting.hashtags.all():
            hashtags.append({"name": hashtag.name, "id": hashtag.id})
        postdata['hashtags'] = hashtags
        return HttpResponse(json.dumps(postdata), content_type="application/json")
