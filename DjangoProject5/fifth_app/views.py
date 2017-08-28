# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django imports
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

import os


APP_DIR = os.path.basename(os.path.dirname(__file__))


from fifth_app.forms import UserForm, UserProfileInfoForm


def index(request):

    context = {}

    view_path = os.path.join(APP_DIR, 'index.html')

    return render(request, view_path, context)


def users(request):

    context = {}

    view_path = os.path.join(APP_DIR, 'users.html')

    return render(request, view_path, context)


def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:

                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
            print registered

        else:
            print user_form.errors, profile_form.errors

    else:

        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }

    view_path = os.path.join(APP_DIR, 'registration.html')

    return render(request, view_path, context)


@login_required
def special(request):

    return HttpResponse('You are logged in! Nice!')


@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:

            login(request, user)

            return HttpResponseRedirect(reverse('index'))

        elif user:

            return HttpResponse('ACCOUNT NOT ACTIVE')

        else:

            print('Someone tried to login and failed!')
            print('Username: {} | Password: {}'.format(username, password))
            return HttpResponse('INVALID LOGIN DETAILS SUPPLIED!')

    context = {}

    view_path = os.path.join(APP_DIR, 'login.html')

    return render(request, view_path, context)