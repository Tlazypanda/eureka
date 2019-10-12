from rest_framework import serializers
from .models import Articles,ArticleHistory,Bookmark

class ArticlesSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()
    def get_is_bookmarked(self, obj):
        if Bookmark.objects.filter(article_id = obj.id).exists():
            return 1
        else:
            return 0
    class Meta:
        model = Articles
        fields = '_all_'

class ArticleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleHistory
        fields = '_all_'

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '_all_'
