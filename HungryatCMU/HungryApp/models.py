from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from models import *


# ========================================
# 3 USERS (w/permissions):
#
# Student, is_student
# Administrator, is_admin
# RestaurantEmployee, is_employee
# ========================================

class Administrator(models.Model):
  
    GENDERS = (('M', 'Male'), ('F', 'Female'), ('N', 'N/A'))
    
    # user.is_staff --> user is administrator
    user = models.OneToOneField(User)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    cell_phone = models.CharField(max_length=15)
    home_phone = models.CharField(max_length=15)
    
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)
        
    class Meta:
        permissions = (
            ("is_admin", "Admin User"),
        )
        
        
class Student(models.Model):
    
    GENDERS = (('M', 'Male'), ('F', 'Female'), ('N', 'N/A'))
    STUDENT_YEARS = (('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate'))
    
    user = models.OneToOneField(User)
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS)
    cell_phone = models.CharField(max_length=15)
    student_year = models.CharField(max_length=2, choices=STUDENT_YEARS)
    
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)
        
    class Meta:
        permissions = (
            ("is_student", "Student User"),
        )
        
        
class Location(models.Model):
    
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    building_name = models.CharField(max_length=80)
    location_description = models.TextField()
    floor = models.CharField(max_length=4, blank=True)
    room = models.CharField(max_length=8, blank=True)
    wheelchair_accessible = models.BooleanField(default=False)

    def __unicode__(self):
      if self.floor:
        return "%s, Floor %s" % (self.building_name, self.floor)
      else:
        return self.building_name
        
        
class Restaurant(models.Model):

    CUISINES = (('BR', 'Breakfast'), ('AM', 'American'), ('IN', 'Indian'), ('AS', 'Asian'), ('ME', 'Mexican'))

    location = models.ForeignKey(Location)
    restaurant_name = models.CharField(max_length=80)
    restaurant_picture = models.ImageField(upload_to='restaurant-pictures', null=True, blank=True)
    has_vegetarian = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)
    cuisine = models.CharField(max_length=2, choices=CUISINES)
    
    def __unicode__(self):
        return self.restaurant_name
        
        
class OperatingHours(models.Model):

    DAYS_OF_WEEK = ((1, "Sunday"), (2, "Monday"), (3, "Tuesday"), (4, "Wednesday"), (5, "Thursday"), (6, "Friday"), (7, "Saturday"))

    restaurant = models.ForeignKey(Restaurant)
    from_day = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    to_day = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    open_hour = models.PositiveSmallIntegerField(validators=[MaxValueValidator(48)])
    close_hour = models.PositiveSmallIntegerField(validators=[MaxValueValidator(48)])
    
    # -------------------------
    # TODO: Helper methods for outputting friendly strings
    # -------------------------
    
    # -------------------------
    # TODO: Helper methods for converting between open/close_hour
    #       and 48 possible half-hour times (12:30pm, 12:30am)
    # -------------------------
    
    
class RestaurantEmployee(models.Model):
    
    user = models.OneToOneField(User)
    restaurant = models.ForeignKey(Restaurant)
    date_of_birth = models.DateField(null=True)
    cell_phone = models.CharField(max_length=15)
    home_phone = models.CharField(max_length=15)
    is_manager = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)
        
    class Meta:
        permissions = (
            ("is_employee", "Employee User"),
        )
            
        
class FoodItem(models.Model):
    
    restaurant_id = models.ForeignKey(Restaurant, related_name='food_items')
    item_name = models.CharField(max_length=80)
    item_description = models.TextField()
    is_vegetarian = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    prep_time = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    picture = models.ImageField(upload_to="food-item-photos", blank=True)
    
    def __unicode__(self):
        return self.item_name
        
        
class Order(models.Model):
    
    ORDER_STATUSES = (('NP','NotPlaced'),('PL', 'Placed'), ('CP', 'Completed'), ('LT', 'Late'), ('CN', 'Cancelled'))
    
    food_items_inorder = models.ManyToManyField(FoodItem)
    student_id = models.ForeignKey(Student)
    time_placed = models.DateTimeField(blank=True,null=True)
    time_completed = models.DateTimeField(blank=True,null=True)
    is_delivery = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=ORDER_STATUSES, default='NP')
    restaurant_id = models.ForeignKey(Restaurant,blank=True,null=True)

