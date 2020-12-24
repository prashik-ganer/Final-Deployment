from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from shop.models import Orders, OrderUpdate


class OrderStatusForm(ModelForm):
    
    class Meta:
        model = Orders
        fields = '__all__'
        exclude = ['seller','email','name','zip_code']



class OrderUpdatesForm(ModelForm):
    
    class Meta:
        model = OrderUpdate
        fields = '__all__'