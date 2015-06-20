from django.shortcuts import render, redirect
from bookmark.models import Bookmark
from .models import Click


def click_tracker(request, short_id):
    bookmark = Bookmark.objects.get(short=short_id)
    click = Click()
    click.addres = request.META.get('REMOTE_ADDR')
    click.browser = request.META['HTTP_USER_AGENT']
    if request.user.is_authenticated():
        click.user = request.user.id
    click.save()
    return redirect(bookmark.long)