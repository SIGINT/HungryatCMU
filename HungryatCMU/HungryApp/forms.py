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
    andrew_id = forms.CharField(max_length = 20,
                                label = "Andrew ID",
                                widget = forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=200,
                                widget = forms.TextInput(attrs={'class':'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}))
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput(attrs={'class':'form-control'}))


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