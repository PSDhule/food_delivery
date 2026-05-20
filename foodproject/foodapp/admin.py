from django.contrib import admin
from .models import Food, Order, Contact, comment

# Register your models here.
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(comment)