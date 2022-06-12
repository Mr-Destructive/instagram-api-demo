from django.shortcuts import render
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from instagram_private_api import Client, ClientCompatPatch
from api.models import Feed
import requests
from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(CreateView):
    form_class = UserForm
    template_name = "user_creation.html"
    success_url = "/"

    def form_valid(self, form):

        api = Client(form.instance.username, form.instance.instagram_password)
        user_id = api.username_info(form.instance.username)["user"]["pk"]
        form.instance.user_id = user_id
        return super(Home, self).form_valid(form)


class InstaFeedView(LoginRequiredMixin, ListView):
    model = Feed
    template_name = "feed_list.html"

    def get_context_data(self, **kwargs):
        url = f"http://127.0.0.1:8000/api/{self.request.user.id}"
        feed = requests.get(url)
        context = {}
        feed_list = Feed.objects.filter(user=self.request.user).all()
        feed_list = feed_list[0].posts.all()
        context["feed"] = feed_list
        return context
