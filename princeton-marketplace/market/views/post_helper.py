from market.models import *
### FOR MODULARIZATION!! :D :D :D
def return_posts(request, num_items, postings):
    length = 0
    i = 0
    try:
        i=int(num_items)
    except ValueError:
        i = 0
    if (i == 0):
        length = len(postings)
    else:
        length = i

    i = 0
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
        postdata['selling'] = posting.is_selling # should all be false
        postdata['open'] = posting.is_open # should all be true
        postdata['category'] = {"name": posting.category.name, "id": posting.category.id}
        postdata['id'] = posting.id
        #postdata['image'] = posting.picture
        hashtags = []
        for hashtag in posting.hashtags.all():
            hashtags.append({"name": hashtag.name, "id": hashtag.id})
        postdata['hashtags'] = hashtags
        response_list.append(postdata)
        i=i+1
        if (i >= length):
            break
    return response_list

### FOR MODULARIZATION TOO!! :D :D :D Sorts the posts based on string "sorting"
def sort_posts(request, sorting, postings):
    sorted_postings = postings
    if (sorting=="" or sorting=="date"):
        sorted_postings = sorted_postings.order_by('-date_posted')
    if (sorting=="category"):
        sorted_postings = sorted_postings.order_by('category__name')
    if (sorting=="price"):
        sorted_postings = sorted_postings.order_by('price')
    if (sorting=="expiration"):
        sorted_postings = sorted_postings.order_by('date_expires')
    return sorted_postings