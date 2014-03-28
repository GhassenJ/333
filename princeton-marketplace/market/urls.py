from django.conf.urls import patterns, url

from market import views

urlpatterns = patterns('',
    url(r'^$', views.display_postings, name='index'),
    url(r'^create_posting/$', views.create_posting, name='create_posting'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^posting/(?P<posting_id>\d+)/$', views.posting_detail, name='posting_detail'),
    url(r'^user/(?P<user_id>\d+)/$', views.user_detail, name='user_detail'),
)

