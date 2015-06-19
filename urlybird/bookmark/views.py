from django.shortcuts import render
import operator
from django.db.models import Avg, Count
from .models import Bookmark
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')

class BookmarkCreate(CreateView):
    model = Bookmark
    fields = ['long', 'title', 'description']
    success_url = '/index/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BookmarkCreate, self).form_valid(form)

class BookmarkUpdate(UpdateView):
    model = Bookmark
    fields = ['long', 'title', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BookmarkUpdate, self).form_valid(form)

class BookmarkDelete(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('/index/')

