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
from hashids import Hashids
from click.models import Click

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')

class BookmarkCreate(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = ['long', 'title', 'description']
    success_url = '/index/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        hashids = Hashids(min_length = 4, salt="browndogbella")
        previous = Bookmark.objects.latest('id')
        previousid = previous.id
        if previous.id is None:
            previousid = 0
        form.instance.short = hashids.encrypt(previousid + 1)
        messages.add_message(self.request, messages.SUCCESS,"You created a bookmark!")
        return super(BookmarkCreate, self).form_valid(form)

class BookmarkUpdate(LoginRequiredMixin, UpdateView):
    model = Bookmark
    fields = ['long', 'title', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BookmarkUpdate, self).form_valid(form)

class BookmarkDelete(LoginRequiredMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('/index/')

class BookmarkList(ListView):
    model = Bookmark
    context_object_name = 'bookmarks'

class UserBookmarkList(ListView):
    model = Bookmark
    context_object_name = 'user_bookmarks'
    template_name = 'bookmark/user_bookmarks.html'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Bookmark.objects.filter(user_id=user_id).order_by('-created')
        return queryset

def bookmark_display(request, pk):
    bookmark = Bookmark.objects.get(pk=pk)
    number_clicks = Click.objects.filter(bookmark__id=pk).count()

    return render(request, "bookmark/bookmark_display.html",
                  {"bookmark": bookmark,
                   "number_clicks": number_clicks})