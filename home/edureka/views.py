from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import  api_view, authentication_classes, permission_classes
from . import models
from . import serializers
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
import requests
from rest_framework.response import Response
from .ginger import main

def response_500(log_msg, e):

    return Response({'status': 'error','message': 'Something went wrong.'}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


def response_400(message, log_msg, e):

    return Response({'status': 'error','message': message}, status= status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_articles(request):
    try:

        headers = {
          'Content-Type': 'application/json',
        }
        response = requests.get('http://www.mediawiki.org/w/api.php?action=query&list=search&srsearch=nelsonmandela&srlimit=1&utf8=&format=json',  headers=headers)
        response = response.json()

        for res in response['search']:
            Article.objects.create(data=res)

        queryset = Article.objects.all()

        return Response({"message":ArticleSerializer(queryset,many=True).data})
    except Exception as e:
        return Response({"message":"An error occured" + str(e)})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def add_article_history(request,article_id):
        article = Articles.objects.get(id = article_id)
        articleHistory = ArticleHistory()
        articleHistory.article = article
        articleHistory.user = request.user
        return Response(UserSerializer(article).data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def add_article_bookmark(request,article_id):
    try:
        article = Articles.objects.get(id = article_id)
        bookmark = Bookmark()
        bookmark.article = article
        bookmark.user = request.user
        return Response(BookmarkSerializer(bookmark).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":"An error occured. " + str(e)})

@api_view(['GET'])
def get_articles(request):
    try:
        articles = Articles.objects.all()
        return Response({"message":ArticleSerializer(articles,many=True).data},status = status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":"An error occured. " + str(e)})

@api_view(['GET'])
def get_bookmarks(request):
    try:
        bookmarks = Bookmark.objects.filter(user = request.user)
        return Response({"message":BookmarkSerializer(bookmarks,many=True).data},status = status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":"An error occured. " + str(e)})

@api_view(['GET'])
def get_article_history(request):
    try:
        history = ArticleHistory.objects.filter(user = request.user)
        return Response({"message":ArticleHistorySerializer(history,many=True).data},status = status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":"An error occured. " + str(e)})

@api_view(['DELETE'])
def delete_bookmark(request , bookmark_id):
    try:
        if not(Bookmark.objects.filter(id = bookmark_id).exists):
            return Response({"message":"Bookmark doesn't exist"} , status=status.HTTP_400_BAD_REQUEST)
        bookmark = Bookmark.objects.get(id = bookmark_id)
        bookmark.delete()
        return Response({"message":"Deleted successfully."},status = status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"message":"An error occured. " + str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def vocab_support(request):
        text = request.data['text']
        result = main(text)
        return Response(result, status=status.HTTP_200_OK)
