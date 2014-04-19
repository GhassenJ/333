from django.conf.urls import patterns, url

from market import views

urlpatterns = patterns('',
    url(r'^$', views.display_postings, name='index'),
    url(r'^create_posting/$', views.create_posting, name='create_posting'),
    url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^accounts/login/$', 'django_cas.views.login', name='login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout', name='logout'),


    url(r'^my_open_posts/(?P<num_items>\d+)/$', views.my_open_posts, name='my_open_posts'),
    url(r'^my_locked_posts/(?P<num_items>\d+)/$', views.my_locked_posts, name='my_locked_posts'),
    url(r'^my_responded_posts/(?P<num_items>\d+)/$', views.my_responded_posts, name='my_responded_posts'),
    url(r'^all_buying_posts/(?P<num_items>\d+)/$', views.all_buying_posts, name='all_buying_posts'),
    url(r'^all_selling_posts/(?P<num_items>\d+)/$', views.all_selling_posts, name='all_selling_posts'),
    url(r'^all_categories/$', views.all_categories, name='all_categories'),
    url(r'^all_hashtags/$', views.all_hashtags, name='all_hashtags'),
    url(r'^search_posts/(?P<query>.*)/$', views.search_posts, name='search_posts'),

    url(r'^category_selling_posts/(?P<category_id>\d+)/(?P<num_items>\d+)/$', views.category_selling_posts, name='category_selling_posts'),
    url(r'^category_buying_posts/(?P<category_id>\d+)/(?P<num_items>\d+)/$', views.category_buying_posts, name='category_buying_posts'),
    url(r'^hashtag_selling_posts/(?P<hashtag_id>\d+)/(?P<num_items>\d+)/$', views.hashtag_selling_posts, name='hashtag_selling_posts'),
    url(r'^hashtag_buying_posts/(?P<hashtag_id>\d+)/(?P<num_items>\d+)/$', views.hashtag_buying_posts, name='hashtag_buying_posts'),
    url(r'^posting_detail/(?P<posting_id>\d+)/$', views.posting_detail, name='posting_detail'),
    url(r'^user_detail/(?P<user_id>\d+)/$', views.user_detail, name='user_detail'),
    url(r'^get_reviews/(?P<user_id>\d+)/$', views.get_reviews, name='get_reviews'),
    url(r'^review_detail/(?P<review_id>\d+)/$', views.review_detail, name='review_detail'),

    url(r'^delete_posting/(?P<posting_id>\d+)/$', views.delete_posting, name='delete_posting'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^respond_to_posting/(?P<posting_id>\d+)/$', views.respond_to_posting, name='respond_to_posting'),
    url(r'^remove_responder/(?P<posting_id>\d+)/$', views.remove_responder, name='remove_responder'),
    url(r'^edit_posting/(?P<posting_id>\d+)/$', views.edit_posting, name='edit_posting'),
    url(r'^close_posting/(?P<posting_id>\d+)/$', views.close_posting, name='close_posting'),
    url(r'^write_review/(?P<user_id>\d+)/$', views.write_review, name='write_review'),
)

