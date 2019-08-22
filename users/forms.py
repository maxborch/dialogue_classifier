from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    """
    This class generates the form for the user registration form.
    It is used by the templates:
        -register.html
        -onboard_employee.html
   It is displayed on pages:
        - /register

    The fields for registration are: username, email, password and password confirmation.
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
    This class generates the form for the user profile update form.
    It is used by the templates:
        -profile.html
    It is displayed on pages:
        - /profile
    The fields for update are: username and email.
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class CreateModerator(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
