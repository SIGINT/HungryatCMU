from django.db import models
from django.contrib.auth.models import User
from models import *



# -----------------------------
# TODO: ADMINISTRATOR model
# -----------------------------

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
    date_of_birth = models.DateField()
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
    
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    building_name = models.CharField(max_length=80)
    location_description = models.TextField()
    floor = models.CharField(max_length=4)
    room = models.CharField(max_length=8)
    wheelchair_accessible = models.BooleanField(default=False)

    def __unicode__(self):
      if self.floor:
        return "%s, Floor %s" % (self.building_name, self.floor)
      else:
        return self.building_name
        
        
class Restaurant(models.Model):

    # --------------------
    # TODO: Add add'l cuisine categories if necessary
    # --------------------
    CUISINES = (('BR', 'Breakfast'), ('AM', 'American'), ('IN', 'Indian'), ('AS', 'Asian'))

    location = models.ForeignKey(Location,blank=True, null=True, default=None)
    restaurant_name = models.CharField(max_length=80)
    restaurant_picture = models.ImageField(upload_to='restaurant-pictures', blank=True)
    has_vegetarian = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)
    cuisine = models.CharField(max_length=2, choices=CUISINES)

    # ---------------------
    # TODO: Discuss possible data type(s) for
    #       storing operating_hours - comma separated integers ?
    # ---------------------
    #operating_hours =
    
    def __unicode__(self):
        return self.restaurant_name
        
        
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
    
    restaurant_id = models.ForeignKey(Restaurant)
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
    
    ORDER_STATUSES = (('PL', 'Placed'), ('CP', 'Completed'), ('LT', 'Late'), ('CN', 'Cancelled'))
    
    food_items_inorder = models.ManyToManyField(FoodItem)
    student_id = models.ForeignKey(Student)
    time_placed = models.DateTimeField()
    time_completed = models.DateTimeField()
    is_delivery = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=ORDER_STATUSES)
    
