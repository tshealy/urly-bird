from django.shortcuts import render
import operator
from django.db.models import Avg, Count
# from .models import
from .forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

def user_register(request):

    if request.method == "GET":
        user_form = UserCreationForm()

    elif request.method == "POST":
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            password = user.password
            # The form doesn't know to call this special method on user.
            user.set_password(password)
            user.save()

            # You must call authenticate before login.
            user = authenticate(username=user.username,
                                password=password)
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Congratulations, {}, on creating your Urly-Bird account! You are now logged in.".format(
                    user.username))
            return redirect('/index/')
        #the return renders to template
    return render(request, "bookmark/register.html", {'user_form': user_form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')

