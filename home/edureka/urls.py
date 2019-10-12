from django.urls import include, path
from django.conf.urls import url, include
from .views import get_articles,add_article_bookmark,get_bookmarks,delete_bookmark,add_article_history,get_article_history,vocab_support

urlpatterns = [
url(
    r'^get_articles/$',get_articles),
url(
    r'^add_bookmark/(?P<article_id>\d+)/$',add_article_bookmark),
url(
    r'^bookmarks/$',get_bookmarks),
url(
    r'^delete_bookmark/(?P<bookmark_id>\d+)/$',delete_bookmark),
url(
    r'^add_article_history/(?P<article_id>\d+)/$',add_article_history),
url(
    r'^get_history/$',get_article_history),
url(
    r'^get_vocab_support/$',vocab_support),

]
