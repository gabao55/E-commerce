from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.http import HttpResponse, request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import copy
import uuid
from utils.utils import reset_password

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
            messages.error(
                self.request,
                'Invalid field(s).'
            )
            
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
            
            messages.success(
                self.request,
                "Update successful."
            )

        # New user
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()
            
            messages.success(
                self.request,
                "Registration successful."
            )

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


        return redirect('user:login')

class Login(View):
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.template_name = 'user/login.html'
        self.render = render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Username or password invalid.'
            )
            return redirect('user:create')

        user = authenticate(self.request,
        username=username, password=password)

        if not user:
            messages.error(
                self.request,
                'Username or password invalid.'
            )
            return redirect('user:create')

        login(self.request, user=user)

        messages.success(self.request, "Login successful.")

        if self.request.session.get('cart', {}):
            return redirect('product:shopresume')

        return redirect('product:list')

    def get(self, *args, **kwargs):
        return self.render

class Logout(View):
    def get(self, *args, **kwargs):

        if self.request.session.get('cart'):
            cart = copy.deepcopy(self.request.session.get('cart'))
        else:
            cart = False

        logout(self.request)

        if cart:
            self.request.session['cart'] = cart
            self.request.session.save()
        return redirect('product:list')
        
class ForgotPassword(View): 
    template_name='user/password_reset.html'

    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')

        if not User.objects.filter(email=email).first():
            messages.success(
                self.request,
                'Email sent.'
            )
            return redirect('user:login')

        user = get_object_or_404(User, email=email)

        name = user.first_name
        user.set_password(reset_password(email, name, user))
        user.save()
        
        messages.success(
            self.request,
            'Email sent.'
        )

        return redirect('user:login')

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

class ChangePassword(View):
    template_name = 'user/change_password.html'

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        temporary_password = self.request.POST.get('temporary_password')
        new_password = self.request.POST.get('new_password')
        new_password2 = self.request.POST.get('new_password2')

        if not username or not temporary_password or not new_password or not new_password2:
            messages.error(
                self.request,
                'Please fill all the fields bellow to proceed.'
            )
            return redirect('user:change_password')

        user_authentication = authenticate(
            self.request,
            username=username,
            password=temporary_password
        )

        user = get_object_or_404(User, username=username)

        if user_authentication is None:
            messages.error(
                self.request,
                'Username or temporary password invalid.'
            )
            return redirect('user:change_password')

        if new_password != new_password2:
            messages.error(
                self.request,
                'New password and password confirmation must be the same.'
            )
            return redirect('user:change_password')

        user.set_password(new_password)
        user.save()

        messages.success(
            self.request,
            'Password changed successfully.'
        )

        return redirect('user:login')

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)