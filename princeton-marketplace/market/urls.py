from django.conf.urls import patterns, url

from market import views

urlpatterns = patterns('',
    url(r'^$', views.display_postings, name='index'),
    #url(r'^create_posting/$', views.create_posting, name='create_posting'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
#    url(r'^login/$', 'django_cas.views.login', name='login'),
#    url(r'^logout/$', 'django_cas.views.logout', name='logout'),

    url(r'^my_open_posts/$', views.my_open_posts, name='my_open_posts'),
    url(r'^my_closed_posts/$', views.my_closed_posts, name='my_closed_posts'),
    url(r'^my_responded_posts/$', views.my_responded_posts, name='my_responded_posts'),
    url(r'^all_buying_posts/$', views.all_buying_posts, name='all_buying_posts'),
    url(r'^all_selling_posts/$', views.all_selling_posts, name='all_selling_posts'),
    url(r'^all_categories/$', views.all_categories, name='all_categories'),
    url(r'^all_hashtags/$', views.all_hashtags, name='all_hashtags'),
    url(r'^my_responded_posts/$', views.my_responded_posts, name='my_responded_posts'),

    url(r'^category_selling_posts/(?P<category_id>\d+)/$', views.category_selling_posts, name='category_selling_posts'),
    url(r'^category_buying_posts/(?P<category_id>\d+)/$', views.category_buying_posts, name='category_buying_posts'),
    url(r'^hashtag_selling_posts/(?P<hashtag_id>\d+)/$', views.hashtag_selling_posts, name='hashtag_selling_posts'),
    url(r'^hashtag_buying_posts/(?P<hashtag_id>\d+)/$', views.hashtag_buying_posts, name='hashtag_buying_posts'),
    url(r'^posting_detail/(?P<posting_id>\d+)/$', views.posting_detail, name='posting_detail'),
    url(r'^user_detail/(?P<user_id>\d+)/$', views.user_detail, name='user_detail'),
    url(r'^get_reviews/(?P<user_id>\d+)/$', views.get_reviews, name='get_reviews'),
)

