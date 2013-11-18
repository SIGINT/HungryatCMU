from django import forms
from django.contrib.auth.models import User
from models import *


class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=40,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=40,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length = 20,
                                widget = forms.TextInput(attrs={'class':'form-control'}))
    gender = forms.ChoiceField(widget = forms.RadioSelect,
                                choices=Student.GENDERS)
    student_year = forms.ChoiceField(widget = forms.Select(attrs={'class':'form-control'}),
                                choices = Student.STUDENT_YEARS)
    #andrew_id = forms.CharField(max_length = 20, label = "Andrew ID", widget = forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=200,
                                widget = forms.TextInput(attrs={'class':'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}))
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput(attrs={'class':'form-control'}))
    # -- TODO: cell_phone --> 3rd party lib or RegexField?
    # cell_phone = forms.


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(StudentRegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length = 20,
                                widget = forms.TextInput(attrs={'class':'form-control'}))    
    password1 = forms.CharField(max_length = 200, 
                                label='New Password', 
                                widget = forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm New Password',  
                                widget = forms.PasswordInput(attrs={'class':'form-control'}))


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ForgotPasswordForm, self).clean()
        #if not user_object:
              #do insert or whatever etc.  
        
        username = cleaned_data.get('username')
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("The username '%s' does not exist.Please register for an account if you dont have one!" % username)

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class ResetPasswordForm(forms.Form):  
    username = forms.CharField(max_length = 20,
                                widget = forms.TextInput(attrs={'class':'form-control'}))
    passwordold = forms.CharField(max_length = 200, 
                                label='Old Password', 
                                widget = forms.PasswordInput(attrs={'class':'form-control'}))

    passwordnew1 = forms.CharField(max_length = 200, 
                                label='New Password', 
                                widget = forms.PasswordInput(attrs={'class':'form-control'}))
    passwordnew2 = forms.CharField(max_length = 200, 
                                label='Confirm New Password',  
                                widget = forms.PasswordInput(attrs={'class':'form-control'}))

     
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ResetPasswordForm, self).clean()
        username = cleaned_data.get('username') 
        passwordold = cleaned_data.get('passwordold')
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("The username '%s' or password does not exist.Please register for an account if you dont have one!" % username)
        
        if not user.check_password(passwordold):
            raise forms.ValidationError('Your old password does not match the records')
            
        # Confirms that the two password fields match
        passwordnew1 = cleaned_data.get('passwordnew1')
        passwordnew2 = cleaned_data.get('passwordnew2')
        
        if passwordnew1 and passwordnew2 and passwordnew1 != passwordnew2:
            raise forms.ValidationError("Your New Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data
        
        
class RestaurantForm(forms.Form):
  location = forms.ModelChoiceField(queryset = Location.objects.all(),
                                    empty_label = None,
                                    widget =  forms.Select(attrs={'class':'form-control'}))
                                    
  restaurant_name = forms.CharField(max_length = 80,
                                    widget = forms.TextInput(attrs={'class':'form-control'}))
  restaurant_picture = forms.ImageField(widget=forms.FileInput())
  has_vegetarian = forms.BooleanField()
  #phone = forms.RegexField()
  cuisine = forms.ChoiceField(widget = forms.RadioSelect,
                              choices = Restaurant.CUISINES)
  
  def clean(self):
      # Calls our parent (forms.Form) .clean function, gets a dictionary
      # of cleaned data as a result
      cleaned_data = super(RestaurantForm, self).clean()
      loc = cleaned_data.get('location')
      restaurant_name = cleaned_data.get('restaurant_name')
      restaurant_picture = cleaned_data.get('restaurant_picture')
      has_vegetarian = cleaned_data.get('has_vegetarian')
      cuisine = cleaned_data.get('cuisine')
      # ----------------------
      # TODO: Ensure location exists in system
      # ----------------------
      try:
        location = Location.objects.get(id=loc.id)
      except Location.DoesNotExist:
        raise forms.ValidationError("The location specified does not exist in the system")
        
      return cleaned_data
      
      
class LocationForm(forms.Form):
    latitude = forms.DecimalField(widget = forms.TextInput(attrs={'class':'form-control', 'readonly':'true'}))
    longitude = forms.DecimalField(widget = forms.TextInput(attrs={'class':'form-control', 'readonly':'true'}))
    building_name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    location_description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    floor = forms.CharField(max_length=4,
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    room = forms.CharField(max_length=8,
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    wheelchair_accessible = forms.BooleanField()
    
    def clean(self):
        cleaned_data = super(LocationForm, self).clean()
        return cleaned_data
      
      
class InviteEmployeeForm(forms.Form):
    restaurant = forms.ModelChoiceField(queryset = Restaurant.objects.all(),
                                      empty_label = None,
                                      widget = forms.Select(attrs={'class':'form-control'}))
    is_manager = forms.BooleanField()
    username = forms.CharField(max_length = 20,
                              widget = forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=200,
                            widget = forms.TextInput(attrs={'class':'form-control'}))
                      
    def clean(self):
        cleaned_data = super(InviteEmployeeForm, self).clean()
        res = cleaned_data.get('restaurant')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        is_manager = cleaned_data.get('is_manager')

        try:
            restaurant = Restaurant.objects.get(id=res.id)
        except Restaurant.DoesNotExist:
            raise forms.ValidationError("The restaurant specified does not exist in the system")
        
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
            
        return username
        
        
class EmployeeRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=40,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=40,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}))
    
    # -- TODO: cell_phone --> 3rd party lib or RegexField?
    # cell_phone = forms.
    # home_phone = forms.
    
    password1 = forms.CharField(max_length = 200, 
                                    label='Password', 
                                    widget = forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length = 200, 
                                    label='Confirm Password',  
                                    widget = forms.PasswordInput(attrs={'class':'form-control'}))
    def clean(self):
        cleaned_data = super(EmployeeRegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Your passwords did not match.")
            
        return cleaned_data
        
        
class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        exclude = ('restaurant_id',)
        widgets = {'food_item_pic' : forms.FileInput() }  

#class SearchForm(forms.Form):