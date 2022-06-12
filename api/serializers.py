from rest_framework import serializers
from .models import Post, Caption, Feed 


class CaptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Caption 
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = "__all__"

