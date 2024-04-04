from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import SignupForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            send_activation_email(request, user)
            return redirect('verify-email', user_pk=user.pk)
    else:
        form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if not user.email_is_verified:
                    return redirect('verify-email', user_pk=user.pk)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def send_activation_email(request, user):
    current_site = get_current_site(request)
    email = user.email
    subject = 'Attiva il tuo account'
    message = render_to_string('authentication/verify_email_message.html', {
        'request': request,
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject, message, to=[email])
    email.content_subtype = 'html'
    email.send()


def verify_email(request, user_pk):
    if request.method == 'POST':
        user = get_user_model().objects.get(pk=user_pk)
        if not user.email_is_verified:
            send_activation_email(request, user)
            return redirect('verify-email-done')
        else:
            return redirect('signup')
    return render(request, 'authentication/verify_email.html')


def verify_email_done(request):
    return render(request, 'authentication/verify_email_done.html')


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True   # FIXME: check if this field is required
        user.is_active = True
        user.save()
        messages.success(request, 'La tua email è stata verificata.')
        return redirect('verify-email-complete')
    else:
        messages.warning(request, 'Il link è invalido.')
    return render(request, 'authentication/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'authentication/verify_email_complete.html')


def my_profile(request):
    return render(request, 'authentication/my-profile.html')
