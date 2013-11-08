from django.db import models
from django.contrib.auth.models import User



# -----------------------------
# TODO: ADMINISTRATOR model
# -----------------------------

class Administrator(models.Model):
    
    user = models.OneToOneField(user)
    
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)
        
        
class Student(models.Model):
    
    GENDERS = (('M', 'Male'), ('F', 'Female'), ('N', 'Neither'))
    STUDENT_YEARS = (('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate'))
    
    user = models.OneToOneField(User)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    cell_phone = models.CharField(max_length=15)
    student_year = models.CharField(max_length=2, choices=STUDENT_YEARS)
    
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)
        
        
class RestaurantEmployee(models.Model):
    
    user = models.OneToOneField(User)
    restaurant = models.ForeignKey(Restaurant)
    cell_phone = models.CharField(max_length=15)
    #is_manager = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)
        
        
class Restaurant(models.Model):
    
    # --------------------
    # TODO: Add add'l cuisine categories if necessary
    # --------------------
    CUISINES = (('BR', 'Breakfast'), ('AM', 'American'), ('IN', 'Indian'), ('AS', 'Asian'))
    
    location = models.ForeignKey(Location)
    restaurant_name = models.CharField(max_length=80)
    has_vegetarian = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)
    cuisine = models.CharField(max_length=2, choices=CUISINES)
    
    # ---------------------
    # TODO: Discuss possible data type(s) for
    #       storing operating_hours - comma separated integers ?
    # ---------------------
    #operating_hours =
    
    
class FoodItem(models.Model):
    
    restaurant_id = models.ForeignKey(Restaurant)
    item_name = models.CharField(max_length=80)
    item_description = models.TextField()
    is_vegetarian = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    prep_time = models.PositiveIntegerField()
    price = models.DecimalField()
    picture = models.ImageFile()
    
    def __unicode__(self):
        return self.item_name
        
        
class Order(models.Model):
    
    ORDER_STATUSES = (('PL', 'Placed'), ('CP', 'Completed'), ('LT', 'Late'), ('CN', 'Cancelled'))
    
    food_items = models.ManyToManyField(FoodItem)
    student_id = models.ForeignKey(Student)
    time_placed = models.DateTimeField()
    time_completed = models.DateTimeField()
    is_delivery = models.BooleanField(default=False)
    status = models.CharField( , choices=ORDER_STATUSES)
    
    
class Location(models.Model):
    
    longitude = models.DecimalField(blank=True)
    latitude = models.DecimalField(blank=True)
    building_name = models.CharField(max_length=80)
    location_description = models.TextField()
    floor = models.CharField(max_length=4)
    room = models.CharField(max_length=8)
    wheelchair_accessible = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.building_name
    
    