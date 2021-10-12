from django.contrib.auth.models import User
from django import forms
from django.forms import fields
from . import models
import user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ('user',)

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        help_text=''
    )
    
    password_confirmation = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirm password'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password',
        'password_confirmation', 'email')
    
    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        user_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password_confirmation_data = cleaned.get('password_confirmation')
        email_data = cleaned.get('email')


        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(username=email_data).first()

        error_msg_user_exists = 'Username already registered.'
        error_msg_email_exists = 'E-mail already registered.'
        error_msg_password_match = "Password and password confirmation doesn't match."
        error_msg_password_short = "Password too short, minimum of 6 characters."
        error_msg_required_field = "Field required."

        # Logged users: update
        if self.user:
            if user_db:
                if user_data != user_db.username:
                    new_user = User.objects.filter(username=user_data).first()

                    validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                if email_data != email_db.email:
                        validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password_confirmation_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password_confirmation'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short

        else:
            if user_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field

            if not password_confirmation_data:
                validation_error_msgs['password_confirmation'] = error_msg_required_field

            if password_data != password_confirmation_data:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password_confirmation'] = error_msg_password_match

            if len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))