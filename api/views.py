from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from user.models import Profile
from .serializers import PostSerializer, CaptionSerializer, FeedSerializer
from .models import Post, Caption, Feed
from instagram_private_api import Client, ClientCompatPatch
from datetime import datetime
import json
import requests


class FeedPostView(APIView):
    """
    View a specific Users Feed.
    """

    def get(self, request, pk, format=None):
        user = Profile.objects.get(id=pk)
        api = Client(user.username, user.instagram_password)
        user_id = api.username_info(user.username)["user"]["pk"]

        user_body = {
            "username": user.username,
            "instagram_password": user.instagram_password,
            "user_id": user_id,
        }
        url = f"https://demo-instagram-api.herokuapp.com/user/update/{pk}"
        user = requests.put(url, data=user_body)
        user = json.loads(user.text)
        results = api.user_feed(user_id)
        items = [item for item in results.get("items", [])]
        posts = []
        for item in items:
            ClientCompatPatch.media(item)
            text = item["caption"]["text"]
            if not Caption.objects.filter(text=text).exists():
                media_url = item["image_versions2"]["candidates"][0]["url"]
                created_at = seconds_to_datetime(item["caption"]["created_at"])
                username = item["user"]["username"]

                caption_body = {
                    "text": text,
                    "media_url": media_url,
                    "created": created_at,
                    "username": username,
                }
                caption = requests.post(
                    "https://demo-instagram-api.herokuapp.com/api/caption/create/",
                    data=caption_body,
                )
                caption = json.loads(caption.text)

                post_id = item["pk"]
                code = item["code"]
                caption_list = []
                caption_list.append(caption["id"])
                user_id = item["user"]["pk"]

                post_body = {
                    "post_id": post_id,
                    "user_id": user_id,
                    "code": code,
                    "caption_data": caption_list,
                }
                post_resp = requests.post(
                    "https://demo-instagram-api.herokuapp.com/api/post/create/",
                    data=post_body,
                )
                post = json.loads(post_resp.text)
                posts.append(post["id"])

        if len(posts) > 0:
            feed_body = {"user": pk, "posts": posts}

            response = requests.post(
                "https://demo-instagram-api.herokuapp.com/api/feed/create/",
                data=feed_body,
            )
            feed = json.loads(response.text)
            return Response(response)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def seconds_to_datetime(seconds):
    return datetime.utcfromtimestamp(int(seconds)).strftime("%Y-%m-%d %H:%M:%S")


class CaptionView(APIView):
    def post(self, request, format=None):
        serializer = CaptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedView(APIView):
    def post(self, request, format=None):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
