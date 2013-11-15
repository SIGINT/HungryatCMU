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

from mimetypes import guess_type

from HungryApp.models import *
from HungryApp.forms import *


@login_required
def home(request):
    
    # Sets up list of just the logged-in user's (request.user's) items
    #return render(request, 'HungryApp/index.html')
    restaurants = Restaurant.objects.all()
    context = {'restaurants' : restaurants }
    return render(request, "HungryApp/restaurants.html", context)
    
    
def StudentRegistration(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = StudentRegistrationForm()
        return render(request, 'HungryApp/Studentregister.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = StudentRegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'HungryApp/Studentregister.html', context)

    # If we get here the form data was valid.  Register the user.
    new_user = User.objects.create_user(first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
                                        
    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = True
    new_user.save()
          
    new_student = Student(date_of_birth=form.cleaned_data['date_of_birth'],
                          gender=form.cleaned_data['gender'],
                          student_year=form.cleaned_data['student_year'],
                          user=new_user)
    new_student.save()
        
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
    
    
@login_required
def restaurants(request):
    
    # Simple index --> list all entities in system
    restaurants = Restaurant.objects.all()
    context = {'restaurants' : restaurants }
    return render(request, "HungryApp/restaurants.html", context)
    
    
@login_required
def view_account(request):
  
  current_user = request.user
  context = {'user' : current_user}
  return render(request, "HungryApp/account.html", context)
  
  
# ---------------------------
# TODO: THIS IS TEMPORARY
#   --> Remember to ensure that normal/unprivileged users 
#       (students) are not able to add restaurants to system
# ------------------------------------------
@login_required
def add_restaurant(request):
  context = {}
  
  if request.method == 'GET':
    context['form'] = RestaurantForm()
    return render(request, 'HungryApp/add_restaurant.html', context)
    
  form = RestaurantForm(request.POST, request.FILES)
  context['form'] = form
  
  if not form.is_valid():
    return render(request, 'HungryApp/add_restaurant.html', context)
    
  new_restaurant = Restaurant(location=form.cleaned_data['location'],
                              restaurant_name=form.cleaned_data['restaurant_name'],
                              restaurant_picture=form.cleaned_data['restaurant_picture'],
                              has_vegetarian=form.cleaned_data['has_vegetarian'],
                              cuisine=form.cleaned_data['cuisine'])
  new_restaurant.save()
  
  # --------------------
  # TODO: Render restaurants page
  # --------------------
  #return render(request, "/restaurant", {})
  return redirect("/account")
  
  
@login_required
def edit_restaurant(request, id):
  context = {}
  
  # -------------------
  # TODO: use of 404-friendly errors vs objects.select_for_update() ??
  # -------------------
  #r = Restaurant.objects.select_for_update().filter(restaurant=
  r = get_object_or_404(Restaurant, pk=id)
  
  if request.method == 'GET':
    context['form'] = RestaurantForm()
    return render(request, 'HungryApp/edit_restaurant.html', context)
    
  form = RestaurantForm(request.POST, request.FILES)
  context['form'] = form
  
  if not form.is_valid():
    return render(request, 'HungryApp/edit_restaurant.html', context)
    
  # POST request's form is valid --> update database
  r.update(location=form.cleaned_data['location'],
            restaurant_name=form.cleaned_data['restaurant_name'],
            restaurant_picture=form.cleaned_data['restaurant_picture'],
            has_vegetarian=form.cleaned_data['has_vegetarian'],
            cuisine=form.cleaned_data['cuisine'])
  
  # TODO !!!!!!!!!!!
  return redirect('/restaurants')
    
  
  
@login_required
def get_restaurant_picture(request, id):
  r = get_object_or_404(Restaurant, pk=id)
  
  if not r.restaurant_picture:
    raise Http404
      
  content_type = guess_type(r.restaurant_picture.name)
  return HttpResponse(r.restaurant_picture, mimetype=content_type)
  

@login_required
@transaction.commit_on_success
def add_fooditem(request):
    
    if request.method == "GET":
        context = {'form':FoodItemForm()}
        return render(request, 'HungryApp/add_fooditem.html', context)
        
    new_food_item = FoodItem(restaurant_id= Restaurant.objects.get(id=id))
    form = FoodItemForm(request.POST, request.FILES, instance=new_food_item)
    if not form.is_valid():
        context = {'form':form}
        return render(request, 'HungryApp/add_fooditem.html', context)
   
    form.save()
    return redirect(reverse('display_fooditems'))

@login_required
@transaction.commit_on_success
def edit_fooditem(request, id):
    fooditem_to_edit = get_object_or_404(FoodItem, restaurant_id=request.restaurant, id=id)

    if request.method == 'GET':
        form = FoodItemForm(instance=fooditem_to_edit)  # Creates form from the 
        context = {'form':form, 'id':id}          # existing entry.
        return render(request, 'HungryApp/edit_fooditem.html', context)

    # if method is POST, get form data to update the model
    form = FoodItemForm(request.POST, request.FILES, instance=entry_to_edit)

    if not form.is_valid():
        context = {'form':form, 'id':id} 
        return render(request, 'HungryApp/edit_fooditem.html', context)

    form.save()
    return redirect(reverse('display_fooditems'))

@login_required
def display_fooditems(request):
    
    context = {'food_items':FoodItem.objects.all()}
    return render(request, 'HungryApp/display_fooditems.html', context)        

@login_required
def get_fooditem_photo(request, id):
  food_item = get_object_or_404(FoodItem, pk=id)
  
  if not food_item.picture:
    raise Http404
      
  content_type = guess_type(food_item.picture.name)
  return HttpResponse(food_item.picture, mimetype=content_type)




"""@login_required
def add_food_item(request):
  context = {}
  
  if request.method == 'GET':
    context['form'] = RestaurantForm()
    return render(request, 'HungryApp/add_restaurant.html', context)
    
  form = RestaurantForm(request.POST, request.FILES)
  context['form'] = form
  
  if not form.is_valid():
    return render(request, 'HungryApp/add_restaurant.html', context)
    
  new_restaurant = Restaurant(location=form.cleaned_data['location'],
                              restaurant_name=form.cleaned_data['restaurant_name'],
                              restaurant_picture=form.cleaned_data['restaurant_picture'],
                              has_vegetarian=form.cleaned_data['has_vegetarian'],
                              cuisine=form.cleaned_data['cuisine'])
  new_restaurant.save() """
  
  # --------------------
  # TODO: Render restaurants page
  # --------------------
  #return render(request, "/restaurant", {})
  #"""return redirect("/account")  """