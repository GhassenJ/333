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
    url(r'^my_responded_posts/$', views.my_responded_posts, name='my_responded_posts'),

    url(r'^category_selling_posts/(?P<category_id>\d+)/$', views.category_selling_posts, name='category_selling_posts'),
    url(r'^category_buying_posts/(?P<category_id>\d+)/$', views.category_buying_posts, name='category_buying_posts'),
    url(r'^hashtag_selling_posts/(?P<hashtag_id>\d+)/$', views.hashtag_selling_posts, name='hashtag_selling_posts'),
    url(r'^hashtag_buying_posts/(?P<hashtag_id>\d+)/$', views.hashtag_buying_posts, name='hashtag_buying_posts'),
    url(r'^posting/(?P<posting_id>\d+)/$', views.posting_detail, name='posting_detail'),
    url(r'^user/(?P<user_id>\d+)/$', views.user_detail, name='user_detail'),
)

