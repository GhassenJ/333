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
### REVIEW-BASED VIEWS:
###     -review_detail(request, review_id)
###     -write_review(request, review_id)
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

@login_required
def write_review(request, user_id):
    """
    This view allows an authed user to create a new posting.
    """

    try:
        reviewee = User.objects.get(pk=user_id)
    except Posting.DoesNotExist:
        raise Http404
    else:
        if request.user == reviewee:
            raise Http404
        # If we're doing a POST, read in form data and save it
        if request.method == 'POST':
            review = ReviewForm(data=request.POST)

            # Process a valid form:
            if review.is_valid():
                # Save information from the PostingForm
                tempreview = review.save(commit=False)

                # Save additional information (author, is_open, date_posted)
                tempreview.date = timezone.now()
                tempreview.author = request.user
                tempreview.reviewee = reviewee

                # Save the M2M fields (hashtag and category)
                tempreview.save()

                newscore = tempreview.rating
                if (len(reviewee.review_reviewee.all()) > 1):
                    newscore = int(((len(reviewee.review_reviewee.all())-1)*reviewee.userprofile.rating + tempreview.rating + 0.0) / (len(reviewee.review_reviewee.all())) + 0.5)
                reviewee.userprofile.rating = newscore
                reviewee.userprofile.save()

                if request.is_ajax():
                    return HttpResponse('OK')
                else:
                    return HttpResponseRedirect(reverse('market:index', args=''))
            # Return Errors
            else:
                if request.is_ajax():
                    errors_dict = {}
                    if review.errors:
                        for error in review.errors:
                            e = review.errors[error]
                            errors_dict[error] = unicode(e)
                    return HttpResponseBadRequest(json.dumps(errors_dict))
                else:
                    print review.errors

        # Otherwise, post the empty form for the user to fill in.
        else:
            form = ReviewForm()

        return render(request, 'market/write_review.html', {'form': form, 'user_id': user_id})
