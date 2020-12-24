from django.db import models
from django.contrib.auth.models import User

from accounts.models import Customer, Seller

# Create your models here.
class Product(models.Model):
    seller = models.ManyToManyField(Seller)
    product_id = models.AutoField
    product_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")
    inStock = models.BooleanField()

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default=" ")


    def __str__(self):
        return self.name

class Orders(models.Model):
    STATUS = (
        ('Pending', 'Pending'),                  
        ('Out for delivery', 'Out for delivery'),                    
        ('Delivered', 'Delivered'),
        )
    MODE = (
        ('Pickup', 'Pickup'),                  
        ('Delivery', 'Delivery'),
        )
    seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount= models.IntegerField(default=0)
    name= models.CharField(max_length=90)
    email= models.CharField(max_length=111)
    
    address= models.CharField(max_length=111)
    zip_code= models.CharField(max_length=111)  
    phone= models.IntegerField(default=0)
    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS, default="Pending")
    mode = models.CharField(max_length=200, null=True, blank=True, choices=MODE)
    order_qr = models.ImageField(default="default_profile.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return "Order from : " + self.name
    


class OrderUpdate(models.Model):
    seller = models.ForeignKey(Seller, null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Order id = " + str(self.order_id) + " - " + self.update_desc


class Cart(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    cart_items = models.CharField(max_length=5000)

    def __str__(self):
        return str(self.customer.name)



class Customer_QR(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    items_json_qr = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return str(self.customer.name)