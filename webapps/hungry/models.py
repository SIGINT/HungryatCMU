from django.db import models
from django.contrib.auth.models import User


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
    
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)
        
        
class Restaurant(models.Model):
    
    #CUISINES =
    
    #location = models.ForeignKey(Location)
    restaurant_name = models.CharField(max_length=50)
    has_vegetarian = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)
    #cuisine = 
    #operating_hours = 
    
    
class FoodItem(models.Model):
    
    restaurant_id = models.ForeignKey(Restaurant)
    item_name = models.CharField(max_length=50)
    description = models.TextField()
    is_vegetarian = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    prep_time = models.PositiveIntegerField()
    price = models.DecimalField()
    
    def __unicode__(self):
        return self.item_name
        
        
class Order(models.Model):
    
    food_item_id = models.ForeignKey(FoodItem)
    student_id = models.ForeignKey(Student)
    time_placed = models.DateTimeField()
    time_completed = models.DateTimeField()
    is_delivery = models.BooleanField(default=False)
    #status = models.CharField( , choices=ORDER_STATUSES)
    
    
class Location(models.Model):
    
    #
    # TODO
    #
    