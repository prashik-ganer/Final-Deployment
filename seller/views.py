from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from accounts.decorators import unauthenticated_user, allowed_users, admin_only

# Extra implemented
from .forms import OrderStatusForm, OrderUpdatesForm
from shop.models import Orders, Product, OrderUpdate, Customer_QR
from accounts.models import Seller, Order, Customer
import json
import pyqrcode
from .filters import OrdersFilter


from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def home(request):
    sellers =  Seller.objects.all()
    print(sellers)

    context = {'sellers': sellers}


    return render(request, 'seller/index.html', context)

def seller_profile(request, seller_profile):   
    #     order_items_list.append(p)
    # print("order_items_list : ", order_items_list)
    # j = json.dumps(order_items_list)
    # print("order", order)
    
    
    seller = Seller.objects.get(id=seller_profile)
    # print(seller)
    order = seller.orders_set.all()
    seller_email = seller.seller_email
    seller_phone = seller.seller_phone
    # items_json = order.items_json
    order_count = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()

    # order_json = order.items_json
    orders_list=[]
    for orders in order:
        print(orders)
        orders_list.append(orders)
        # x = {x.items_json for x in orders}                                       # Set comprehension
    print("orders_list")
    print("orders_list", orders_list)

    myFilter = OrdersFilter(request.GET, queryset=order)
    order = myFilter.qs

    # cats = {(item.order_id:item.items_json) for item in orders_list}                                       # Set comprehension
    # print("cats : ", cats)
    # catprods = Product.objects.values('category', 'id')
    # # print(cats)
    # for cat in cats:
    #     prod = Product.objects.filter(category=cat)
    #     n = len(prod)
    #     nSlides = n // 4 + ceil((n / 4) - (n // 4))
    #     allProds.append([prod, range(1, nSlides), nSlides])

    dicts = {}
    order_items_list = []
    for i in order:
        order_id = i.order_id
        items_json = i.items_json
        # print("order_id = ", order_id)
        # print("items_json = ", items_json)
        order_items_list.append(order_id)
        dicts[order_id]=items_json
    # print(dicts)
    dumped_dict = json.dumps(dicts)
    # print("dumped_dict", dumped_dict)
    replaced_dict = dumped_dict.replace("\\", " ")
    dicts1 = replaced_dict.replace("\"{","[{")
    dicts2 = dicts1.replace("}\"","}]")
    # print("dicts2",dicts2)

    # print("order_items_list : ",order_items_list)
    
    
    # print(seller_phone)
    # dumped = json.dumps(order_items_list)
    # # print("dumped order_items_list : ", dumped)
    # # print(type(dumped))
    # replaced1 = dumped.replace("[", " ",1)
    # replaced2 = replaced1.replace("\\", " ")
    # replaced_New = replaced2[:-1]
    # # print(replaced_New)
    # new1 = replaced_New.replace("\"{","{")
    # new2 = new1.replace("}\"","}")
    # new3 = new2.replace("{","")
    # new4 = new3.replace("}","")
    # new5 = "{"+ new4 +"}"

    # print(items_json)
    # print(replaced1)
    # print(replaced2)
    # print(type(replaced_New))
    # print(new5)
        
    context={'replaced_New':dicts2,'order':order,'seller_email':seller_email, 'seller_phone':seller_phone, 'order_count':order_count, 'delivered':delivered, 'pending': pending,
            'myFilter':myFilter}

    return render(request, 'seller/seller_profile.html', context)


def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    print(orders)
    print(customers)

    total_customers = customers.count()

    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers': customers, 
    'total_orders':total_orders, 'total_customers':total_customers,
    'delivered':delivered, 'pending':pending}
    return render(request, 'seller/dashboard.html', context)


def products(request):
    seller = request.user.seller
    print("seller : ", request.user.seller)
    products = Product.objects.filter(seller=seller)
    print(products)
    context = {'products':products}
    # return HttpResponse("Products!")
    return render(request, 'seller/seller_products.html', context)

def sellerTracker(request, status):
    updates = OrderUpdate.objects.get(update_id=status)
    allupdates = OrderUpdate.objects.filter(update_id=status)
    print("allupdates : ", allupdates)
    print("updates : ", updates)
    form  = OrderUpdatesForm(instance=updates)
    if request.method == 'POST':
        form = OrderUpdatesForm(request.POST, instance=updates)
        if form.is_valid():
            form.save()
            return redirect('/seller')
    context = {'form':form}
    return render(request, 'seller/seller_tracker.html', context)


def updateStatus(request, status):
    statusorder = Orders.objects.get(order_id=status)
    form = OrderStatusForm(instance=statusorder)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=statusorder)
        if form.is_valid():
            form.save()
            return redirect('/seller')
    context = {'form':form}
    return render(request, 'seller/update_status.html', context)



