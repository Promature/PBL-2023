from django.db import models
from django.contrib.auth.models import AbstractUser 
from myApp.manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid



# Create your models here.
#create custom user model
class SignupUser(models.Model):
    name = models.CharField(max_length=122)
    #lname = models.CharField(max_length=122)
    email= models.CharField(max_length=122)
    password = models.CharField(max_length=122)
    

    def __str__(self):
        return self.name


class bookView(models.Model):
    book_id = models.AutoField
    name = models.CharField(max_length=122)
    author = models.CharField(max_length=122)
    bookimage = models.ImageField(upload_to="images/",default="")
    genre = models.CharField(max_length=122,default="")
    pub_date = models.DateField() 
    price = models.DecimalField(max_digits=8, decimal_places=2)
    desc = models.CharField(max_length=10000)
    digital = models.BooleanField(default=False, null = True, blank = False)
    time_used = models.CharField(max_length = 9,default="0 D", null=True, blank = True)
    #no need to specify buyer and seller instead r\use reverse relation 
    #book = Book.objects.....
    #buyer = book.bought_by.all()

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    username = None
    name = models.CharField(max_length=122, null = True,unique=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=14)
    first_name = models.CharField(max_length = 100,blank=True, null=True)
    last_name = models.CharField(max_length = 100,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    books_bought = models.ManyToManyField('bookView', related_name='bought_by')
    books_sold = models.ManyToManyField('bookView', related_name='sold_by')
    area_live = models.CharField(max_length=250)
    
    #profile pic, bio, is_verified

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

class Customer(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, null = True)
    email = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.user.name if self.user else ''
    
# for creating customer associated with each newly crreated user
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        name = instance.name  
        email = instance.email  

        customer = Customer.objects.create(user=instance, name=instance.name, email=email)
        customer.name = name
        customer.save()
        Order.objects.create(customer=instance.customer)

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True,blank = True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null = True, unique=True, default=uuid.uuid4)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([1 for item in orderitems])
        return total

class OrderItem(models.Model):
    product =models.ForeignKey(bookView, on_delete=models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True)
    date_added = models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete =models.SET_NULL,null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    address = models.CharField(max_length=200,null = False)
    city = models.CharField(max_length=200,null = False)
    state = models.CharField(max_length=200,null = False)
    zipcode = models.CharField(max_length=200,null = False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address