from django.urls import path
from .views import FeedPostView, CaptionView, PostView, FeedView

urlpatterns = [
        path("<int:pk>", FeedPostView.as_view(), name="feed"),
        path("caption/create/", CaptionView.as_view(), name="caption"),
        path("post/create/", PostView.as_view(), name="post"),
        path("feed/create/", FeedView.as_view(), name="feed"),
]
