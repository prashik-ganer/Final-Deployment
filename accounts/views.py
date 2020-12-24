from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only

# Extra implemented
from shop.models import Orders, OrderUpdate, Product, Cart
from .filters import OrderFilter
# Create your views here.

def registrationPage(request):
    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    return render(request, 'accounts/login.html')



@login_required(login_url='/')
# @admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers': customers, 
    'total_orders':total_orders, 'total_customers':total_customers,
    'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='/')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    print("request.user ----> ", request.user)
    print("request.user.customer ----> ", request.user.customer)
    orders = request.user.customer.order_set.all()
    print(orders)
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'total_orders':total_orders,
    'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='/')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    # not own
    print("request.user ----> ", request.user)
    print("request.user.customer ----> ", request.user.customer)
    orders = request.user.customer.orders_set.all()
    print(orders)
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context2 = {}


    # own
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form, 'orders':orders, 'total_orders':total_orders,
    'delivered':delivered, 'pending':pending}


    return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='/')
# @allowed_users(allowed_roles=['customer'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})



def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context={'customer': customer, 'orders':orders, 
    'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        # print('Printing POST: ',request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        # print('Printing POST: ',request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/accounts')
    context={'form':form}
    return render(request, 'accounts/order_form.html', context)



def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/accounts')
    context ={'item': order}
    return render(request, 'accounts/delete.html', context)
    # return HttpResponse("deleteOrder", pk)


