from django.contrib.auth.models import User
from django.db import models

class Food(models.Model):

    name=models.CharField(max_length=100)

    category = models.CharField(max_length=100)

    price=models.IntegerField()

    image=models.ImageField(upload_to='food/')

    def __str__(self):
        return self.name

class Order(models.Model):
    food_name = models.CharField(max_length=100)

    price = models.IntegerField()

    quantity = models.IntegerField()

    total = models.IntegerField()

    image = models.ImageField(upload_to='orders/')

    rating = models.IntegerField(default=0)


class Contact(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    message = models.TextField()

    def __str__(self):

        return self.name
    
class comment(models.Model):
     
    name = models.CharField(max_length=100)

    comment = models.TextField()

    def __str__(self):
        return self.name

    


