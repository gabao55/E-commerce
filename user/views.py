from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import copy

from . import models
from . import forms
import user

# Create your views here.

class ProfileBase(View):
    template_name = 'user/create.html'
    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.profile = 0
        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        if self.request.user.is_authenticated:
            self.profile = models.UserProfile.objects.filter(
                user=self.request.user
                ).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile)
            }
        else:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None)
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'user/update.html'

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render


class Create(ProfileBase):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.profileform.is_valid():
            return self.render

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # User logged
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, 
            username=self.request.user.username
            )
            
            user.username = username

            if password:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if not self.profile:
                self.profileform.cleaned_data['username'] = username
                profile = models.UserProfile(**self.profielform.cleaned_data)
                profile.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.username = username
                profile.save()

        # New user
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()

        if password:
            authenticate_user = authenticate(
                self.request,
                username=username,
                password=password
            )

            if authenticate_user:
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()
        return self.render

class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')

class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')