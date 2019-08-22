# Function profile() is adapted from https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
# Function register() and activate() adapted from
# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm, CreateModerator
from Dialogue_Classifier.settings import EMAIL_HOST_USER
from emails.emails import send_mail

# from django.contrib.auth.models import Group
# from django.views.generic import ListView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from users.tokens import account_activation_token
# from django.utils.encoding import force_text
# from django.utils.http import urlsafe_base64_decode


# def register(request):
#     """Generates the data for a user registration form which is displayed at /register
#     Uses the register.html template."""
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.is_active = False
#             user.save()
#             #username = form.cleaned_data.get('username')
#             u_id = user.pk
#             current_site = get_current_site(request)
#
#             send_mail(subject=f"Please verify your Dialogue Classifier account",
#                       email_template_name='catalogue/emails/account_activation_email.txt',
#                       context={'user': user, 'site_url': current_site.domain,
#                                'uid': urlsafe_base64_encode(force_bytes(u_id)).decode(),
#                                'token': account_activation_token.make_token(user), }, from_email=EMAIL_HOST_USER,
#                       to_email=form.cleaned_data.get('email'),
#                       html_email_template_name='catalogue/emails/account_activation_email.html')
#             return redirect('account_activation_sent')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {'u_form': u_form}
    return render(request, 'users/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'p_form': form
    })


def onboard_user(request):
    if request.method == 'POST':
        form = CreateModerator(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            # user.groups.add(Group.objects.get(name='administrator'))
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email')
            send_mail(subject=f"Moderator Account Created",
                      email_template_name='users/emails/moderator_created.txt',
                      context={'username': username, 'password': password, 'site_url': request.get_host},
                      from_email=EMAIL_HOST_USER,
                      to_email=user_email, html_email_template_name='users/emails/moderator_created.html')

            messages.success(request, f'New User Created Successfully')
            return redirect('create-user')
    else:
        form = UserRegisterForm(initial={'password1': 'Test1234!', 'password2': 'Test1234!'})
    return render(request, 'users/create-user.html', {'form': form})

# def account_activation_sent(request):
#     return render(request, 'users/account_activation_sent.html')
#
#
# def activate(request, uidb64, token):
#     uid = force_text(urlsafe_base64_decode(uidb64))
#     user = User.objects.get(pk=uid)
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.profile.email_confirmed = True
#         user.save()
#         messages.success(request, 'Account successfully validated! You can now log in with your credentials')
#         return redirect('login')
#     else:
#         return render(request, 'users/account_activation_invalid.html')
