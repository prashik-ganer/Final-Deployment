from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="https://res.cloudinary.com/dbvh7sfop/image/upload/v1609412216/media/kkhypdgpvhg2b7pjp27m.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

class Seller(models.Model):
    seller_user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=200, null=True)
    seller_phone = models.CharField(max_length=200, null=True)
    seller_email = models.CharField(max_length=200, null=True)
    seller_profile_pic = models.ImageField(default="default_profile.png", null=True, blank=True)
    seller_date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.seller_user)



class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)
        
class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),                   
        ('Outdoor', 'Outdoor'),
        )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)


    def __str__(self):
        return str(self.name)



class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),                  
        ('Packed', 'Packed'),                    
        ('Delivered', 'Delivered'),
        )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.product.name)
