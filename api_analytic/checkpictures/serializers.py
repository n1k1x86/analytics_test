from rest_framework import serializers
from .models import Post, PostReview


class PostSerializer(serializers.ModelSerializer):

    @staticmethod
    def get_author_name(obj):
        return obj.author.username

    author = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'description', 'author', 'count_likes']


class PostReviewSerializer(serializers.ModelSerializer):

    @staticmethod
    def get_author_name(obj):
        return obj.author.username

    author_name = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = PostReview
        fields = ['id', 'author', 'author_name', 'review_text']
