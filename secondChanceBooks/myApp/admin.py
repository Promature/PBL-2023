from django.contrib import admin
from myApp.models import *
# Register your models here.

admin.site.register(SignupUser)
admin.site.register(bookView)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Customer)