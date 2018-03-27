from __future__ import unicode_literals
from django.db import models
import re
import datetime

class UserManager(models.Manager):
    def register(self, postData):
        errors = {}
        userList = User.objects.filter(email = postData['email'])

        email_regex = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be more than 2 characters"  
        if len(postData['password']) < 8:
            errors["password"] = "Password should be more than 8 characters"
        if postData['password'] != postData['confpw']:
            errors["password"] = "Passwords must match"
        if len(postData['email']) < 1:
            errors["email"] = "Email address field is required"
        if len(userList) > 0:
            errors["email"] = "There can only be one user per email address"
        if not email_regex.match(postData['email']):
            errors["email"] = "Email is invalid."
        return errors

    def login(self, postData):
        errors = {}
        return errors 

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_level = models.IntegerField()
    objects = UserManager()

class Address(models.Model):
    user = models.ForeignKey(User, related_name='user_addresses')
    address = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    user = models.ForeignKey(User, related_name='user_orders')
    total_price = models.IntegerField()    
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    item = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.ForeignKey(Category, related_name='the_products')
    quantity = models.IntegerField()
    # image = models.ImageField()
    order = models.ForeignKey(Order, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='reviews')
    product = models.ForeignKey(Product, related_name='product_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    review = models.ForeignKey(Review, related_name='comments')
    user = models.ForeignKey(User, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
