from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib import auth

from accounts.models import Token


def send_login_email(request):
    '''send email for login in system'''
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreplay@superlists',
        [email]
    )
    messages.success(
        request,
        'Check your email, you`ll find a message with a link '
        'that will log you into the site.'
    )
    return redirect('/')


def login(request):
    '''login in system'''
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
