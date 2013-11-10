from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import Http404
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, render_to_response
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
import re
from django.db.models import Q
# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.contrib.auth.tokens import default_token_generator
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf 

from HungryApp.models import *
from HungryApp.forms import *



def home(request):
    
    # Sets up list of just the logged-in user's (request.user's) items
    return render(request, 'HungryApp/index.html')

def StudentRegistration(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = StudentRegistrationForm()
        context['action'] = "/register"
        context['submit_text'] = "Register"
        return render(request, 'HungryApp/Studentregister.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = StudentRegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'HungryApp/Studentregister.html', context)

    # If we get here the form data was valid.  Register the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])

    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = True

    new_user.save()
    
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
    Welcome to Hungry@CMU.  Please click the link below to
    verify your email address and complete the registration of your account:

    http://%s%s """%(request.get_host(),reverse('confirm', args=(new_user.username, token)))
    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="cmurugan@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'HungryApp/NeedsConfirmation.html', context) 


def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'HungryApp/EmailConfirmed.html', {})


def forgotpassword(request):
    context = {}
    
    errors = []
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = ForgotPasswordForm()
        return render(request, 'HungryApp/ForgotPassword.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = ForgotPasswordForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'HungryApp/ForgotPassword.html', context)

    # If we get here the form data was valid.  Register the user.
    Password_forgot_user = User.objects.get(username=form.cleaned_data['username'])  

    if not Password_forgot_user :
        errors.append('The user did not exist in your todo list.')  
        context['form'] = ForgotPasswordForm()
        return render(request, 'HungryApp/ForgotPassword.html', context, errors)                                     
    
    Password_forgot_user.set_password(form.cleaned_data['password1']) 
    # Mark the user as inactive to prevent login before email confirmation.
    Password_forgot_user.is_active = False

    Password_forgot_user.save()
    
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(Password_forgot_user)
    
    email_body = """
     Please click the link below to confirm your password change request!
     http://%s%s """%(request.get_host(),reverse('confirm', args=(Password_forgot_user.username, token)))
    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="cmurugan@andrew.cmu.edu",
              recipient_list=[Password_forgot_user.email])

    context['email'] = Password_forgot_user.email 
    return render(request, 'HungryApp/NeedsConfirmation.html', context)    



def resetpassword(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = ResetPasswordForm()
        return render(request, 'HungryApp/ResetPassword.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = ResetPasswordForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'HungryApp/ResetPassword.html', context)
       

    # If we get here the form data was valid.  Register the user.
    Password_reset_user = User.objects.get(username=form.cleaned_data['username'])                                      
    
    Password_reset_user.set_password(form.cleaned_data['passwordnew1']) 
    # Mark the user as active.
    Password_reset_user.is_active = True

    Password_reset_user.save()    
                
    return render(request, 'HungryApp/PasswordConfirmed.html')