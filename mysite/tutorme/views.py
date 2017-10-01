# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from . forms import SignupForm
from . tokens import account_activation_token
from . models import Profile

# Create your views here.

def index(request):
    return render(request, "tutorme/index.html")

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        user = None
        if form.is_valid():
            # eldr: this probably works because SignupForm inherits from UserCreationForm
            user = form.save()
            user.is_active = False
            user.save()
            profile = Profile()
            profile.user = user
            profile.first_name = form.cleaned_data.get("first_name")
            profile.last_name = form.cleaned_data.get("last_name")
            profile.email = form.cleaned_data.get("email")
            profile.birth_date = form.cleaned_data.get("birth_date")
            profile.save()

            current_site = get_current_site(request)
            subject = "Activate your tutorme account"
            message = render_to_string("tutorme/account_activation_email.html", {
                "user" : user,
                "domain": current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message)
            return HttpResponse("account activation sent")

    else:
        form = SignupForm()

    return render(request, "tutorme/signup.html", {"form" : form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return HttpResponse("You have successfully activated your account!")
    else:
        return HttpResponse("Your activation is invalid")
