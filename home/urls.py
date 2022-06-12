from django.urls import path
from .views import Home, InstaFeedView

urlpatterns = [
        path("", Home.as_view(), name="home"),
        path("feed/", InstaFeedView.as_view(), name="feedview"),
]
