import time
from typing import Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from app.models import Article
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
    

class ArticleListView(LoginRequiredMixin, ListView):
    template_name = "app/home.html"
    model = Article
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        time.sleep(2)
        search = self.request.GET.get("search")
        queryset = super().get_queryset().filter(creator=self.request.user)
        if search:
            queryset = queryset.filter(title__search=search)
        return queryset.order_by("-created_at")


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = "app/article_create.html"
    model = Article
    fields = ["title", "content", "status", "twitter_post"]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "app/article_update.html"
    model = Article
    fields = ["title", "content", "status", "twitter_post"]
    success_url = reverse_lazy("home")
    context_object_name = "article"

    def test_func(self):
        return self.request.user == self.get_object().creator



class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "app/article_delete.html"
    model = Article
    success_url = reverse_lazy("home")
    context_object_name = "article"

    def test_func(self):
        return self.request.user == self.get_object().creator
    
    def post(self, request:HttpRequest, *args:str, **kwargs:Any) -> HttpResponse:
        messages.success(request, "Article deleted successfully.", extra_tags="destructive")
        return super().post(request, *args, **kwargs)
        