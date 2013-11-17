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
from django.contrib.admin.views.decorators import staff_member_required

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
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf 

from mimetypes import guess_type

from HungryApp.models import *
from HungryApp.forms import *


@login_required
def home(request):
    context = {}
    
    # Sets up list of just the logged-in user's (request.user's) items
    #return render(request, 'HungryApp/index.html')
    user = request.user
    
    # user.is_staff --> user is administrator
    if user.is_staff:
      return render(request, "HungryApp/admin.html", context)
    else:
      restaurants = Restaurant.objects.all()
      context['restaurants'] = restaurants 
      return render(request, "HungryApp/restaurants.html", context)
            
@staff_member_required
def invite_employee(request):
    context = {}

    if request.method == 'GET':
        context['form'] = InviteEmployeeForm()
        return render(request, 'HungryApp/invite_employee.html', context)

    form = InviteEmployeeForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'HungryApp/invite_employee.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        email=form.cleaned_data['email'])
                                      
    # Not that secure --> come up with alternative for required password field
    #
    # Need way to ensure password is reset/updated when employee registers
    new_user.set_password('temp')
    new_user.is_active = False
    new_user.save()

    new_employee = RestaurantEmployee(user=new_user,
                                    restaurant=form.cleaned_data['restaurant'])
    new_employee.save()

    token = default_token_generator.make_token(new_user)
    email_body = """
    Your're invited to join Hungry@CMU!  Please click the link below to access
    our employee registration page:

    http://%s%s """%(request.get_host(),reverse('register-employee', args=(new_user.username, token)))
    send_mail(subject="Hungry@CMU :: Employee Invitation",
            message= email_body,
            from_email="cmurugan@andrew.cmu.edu",
            recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'HungryApp/invitation_sent.html', context)
  
  
def register_employee(request, username, token):
    logout(request)
    user = get_object_or_404(User, username=username)
    
    if not default_token_generator.check_token(user, token):
        raise Http404    
    
    context = {'username':username, 'token':token}
    
    if request.method == 'GET':
        context['form'] = EmployeeRegistrationForm()
        return render(request, 'HungryApp/employee_register.html', context)
    
    form = EmployeeRegistrationForm(request.POST)
    context['form'] = form
    
    if not form.is_valid():
        return render(request, 'HungryApp/employee_register.html', context)
        
    user.is_active = True
    user.first_name = form.cleaned_data['first_name']
    user.last_name=form.cleaned_data['last_name']
    user.set_password(form.cleaned_data['password1'])
    user.save()
    employee = RestaurantEmployee.objects.select_for_update(user=user)
    employee.update(date_of_birth=form.cleaned_data['date_of_birth'])
                
    return redirect('/')
    
@staff_member_required
def employees(request):
    context = {}
    
    employees = RestaurantEmployee.objects.all()
    context['employees'] = employees
    
    return render(request, 'HungryApp/employees.html', context)
    
@staff_member_required
def students(request):
    context = {}
    
    students = Student.objects.all()
    context['students'] = students
    
    return render(request, 'HungryApp/students.html', context)
    
@staff_member_required
def deactivate_user(request, id):
    user = get_object_or_404(User, pk=id)
    
    if user.is_active:
        user.is_active = False
        user.save()
    
    return redirect('/HungryApp')
    
@staff_member_required
def activate_user(request):
    user = get_object_or_404(User, pk=id)
    
    if not user.is_active:
        user.is_active = True
        user.save()
        
    return redirect('/HungryApp')
    
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
def view_restaurant(request, id):
  context = {}
  r = get_object_or_404(Restaurant, pk=id)
  context['r'] = r
  
  return render(request, 'HungryApp/view_restaurant.html', context)
  
  
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
def add_fooditem(request,id):
    
    if request.method == "GET":
        context = {'form':FoodItemForm(), 'id':id}
        return render(request, 'HungryApp/add_fooditem.html', context)
        
    new_food_item = FoodItem(restaurant_id= Restaurant.objects.get(id=id))
    form = FoodItemForm(request.POST, request.FILES, instance=new_food_item)
    if not form.is_valid():
        context = {'form':form, 'id':id}
        return render(request, 'HungryApp/add_fooditem.html', context)
   
    form.save()
    return redirect(reverse('display_fooditems', args=[id]))

@login_required
@transaction.commit_on_success
def edit_fooditem(request, id):
    fooditem_to_edit = get_object_or_404(FoodItem, id=id)

    if request.method == 'GET':
        form = FoodItemForm(instance=fooditem_to_edit)  # Creates form from the 
        context = {'form':form, 'id':id}          # existing entry.
        return render(request, 'HungryApp/edit_fooditem.html', context)
    
    # if method is POST, get form data to update the model
    form = FoodItemForm(request.POST, request.FILES, instance=fooditem_to_edit)
    context = {'form':form, 'id':id} 
    if not form.is_valid():
        context = {'form':form} 
        return render(request, 'HungryApp/edit_fooditem.html', context)

    form.save()
    return render(request, 'HungryApp/edit_fooditem.html', context)
    #return redirect(reverse('display_fooditems'))

@login_required
def display_fooditems(request,id):

    restaurant = Restaurant.objects.get(id=id)  
    context = {'food_items':FoodItem.objects.filter(restaurant_id = id), 'pk':id }
    #return redirect(reverse('display_fooditems',context))
    return render(request, 'HungryApp/display_fooditems.html', context)        

@login_required
def get_fooditem_photo(request, id):
  food_item = get_object_or_404(FoodItem, pk=id)
  
  if not food_item.picture:
    raise Http404
      
  content_type = guess_type(food_item.picture.name)
  return HttpResponse(food_item.picture, mimetype=content_type)



  # --------------------
  #  Implement Search Functionality 
  # --------------------
  


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['restaurant_name'])
        
    #return render(request, "HungryApp/restaurants.html", context)
        found_entries = Restaurant.objects.filter(entry_query)
        context = {'restaurants' : found_entries } 
     
    return render_to_response('HungryApp/restaurants.html',context)
                          #{ 'query_string': query_string, 'found_entries': found_entries },
                          #context_instance=RequestContext(request)) 


  
  # --------------------
  # TODO: Render restaurants page
  # --------------------
  #return render(request, "/restaurant", {})
  #"""return redirect("/account")  """