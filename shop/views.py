from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Product, Contact, Orders, OrderUpdate, Cart
from math import ceil
import json
import pyqrcode

# Extra Features
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.models import LogEntry
from accounts.models import Customer, Seller

from django.http import JsonResponse
# import numpy

import cloudinary
from seller.forms import OrderQR

import requests
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AllOrdersSerializer

# import cv2
# import numpy as np
# from pyzbar.pyzbar import decode
# import urllib.request



import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()
    






# Create your views here.
class mydict(dict):
        def __str__(self):
            return json.dumps(self)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def index(request):
    
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n // 4 + ceil((n / 4) - (n // 4))



    allProds=[]
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}                                       # Set comprehension
    # print(cats)
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)   
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    
    # user_cart = Cart.objects.values('customer', 'cart_items')
    # cartobjects = {item['customer'] for item in user_cart}                                       # Set comprehension
    # print(cartobjects)
    empty_cart = {""}
    if request.user.is_authenticated:
        customer = request.user.customer
        # cart, created = Cart.objects.update_or_create(
        # customer=customer, defaults={"cart_items": data}
        # )

        # if Carts.objects.filter(customer=customer).exists():
            
        cart_json, created = Cart.objects.get_or_create(customer=customer)
        # cart_json, created = Cart.objects.update_or_create(
        #     customer=customer, 
        # )
        if created:
            cart_json.cart_items = '{}'
            cart = cart_json.cart_items
            user_cart, created = Cart.objects.get_or_create(customer=customer, cart_items=cart)
            params1 = {'allProds': allProds, 'user_cart':user_cart, 'cart': cart, 'product':prod}
            cart_json.delete()
            return render(request, 'shop/index.html', params1)

            # means you have created a new person
        else:
            # person just refers to the existing one
            customer_cart_item = cart_json.cart_items
            print("python object : ", customer_cart_item)
            cart = customer_cart_item.replace("\'", "\"")
            print("replaced : ", cart)
            user_cart, created = Cart.objects.get_or_create(customer=customer, cart_items=customer_cart_item)
            params1 = {'allProds': allProds, 'user_cart':user_cart, 'cart': cart, 'product':prod}
            cart_json.delete()
            return render(request, 'shop/index.html', params1)

        # customer_object = Cart.objects.get(customer=customer)
        print(cart_json)
        # cart_json.cart_items = "{ }"

        # customer_cart_item = cart_json.cart_items
        # print("python object : ", customer_cart_item)
        # cart = customer_cart_item.replace("\'", "\"")
        # print("replaced : ", cart)

        # cart = json.dumps(customer_cart_item)
        # print("two : ", cart)


        
    params = {'allProds': allProds}
    # else:
    #     params = {'allProds': allProds}


    # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    # print(params)
    
    # params = {'allProds': allProds, 'user_cart':user_cart, 'cart':cart}

    return render(request, 'shop/index.html', params)


def scan(request):

    # cap = cv2.VideoCapture(0)
    # while True:
    #     success, img = cap.read()
    #     for qrcode in decode(img):
    #         # print(qrcode.data)
    #         myData = qrcode.data.decode('utf-8')
    #         print(myData)
    #         pts = np.array([qrcode.polygon],np.int32)
    #         pts = pts.reshape((-1,1,2))
    #         cv2.polylines(img,[pts],True,(255,0,255),5)

    #         pts2 = qrcode.rect
    #         cv2.putText(img,myData,(pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)

    #     cv2.imshow('Result : ', img)
    #     cv2.waitKey(1)
    # return render(request, 'shop/scan.html')
    # # return HttpResponse("scan")
    pass





def about(request):
    big_code = pyqrcode.create("sample1", error='L', version=15, mode='binary')
    image_qrcode = big_code.png(f'media/qrcode/sample1.png', scale=3, module_color=[0, 0, 0], background=[0xff, 0xff, 0xcc])
    print("image_qrcode  ::   ", type(image_qrcode))
    context = {'image_qrcode':image_qrcode}
    # cloudinary.config(cloud_name='dbvh7sfop',api_key='773496946691131', api_secret='JZ8lR-OYtXZAOnhkCsnsEYoh70g')
    # cloudinary.uploader.upload("media/qrcode/sample1.png",public_id = 'sample1', folder="media/qrcode")
    # if request.method=='POST':
    return render(request, 'shop/about.html', context)

def contact(request):
    thank = False
    if request.method=="POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        # thank = True
        # print(name, email, phone, desc)

        if len(name)<2 or len(email)<2 or len(phone)<2 or len(desc)<2:
            messages.error(request, "Please fill the form correctly!")
        else:
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request, "Thanks for your valuable feedback. We will get back to you soon.")
    # return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')


def search(request):
    return render(request, 'shop/search.html')

def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    print(product)
    print(product[0])
    print(myid) 

    context = {'myid':myid}
    

    return render(request, 'shop/prodView.html', {'product': product[0]})

def checkout(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # removepunc = request.POST.get('removepunc', 'off')
            # fullcaps = request.POST.get('fullcaps', 'off')
            # if removepunc == "on":
            #     print("removepunc")
            # if fullcaps == "on":
            #     print("fullcaps")
            print(request)
            #To be done
            # seller = Seller.objects.filter(seller_name="shop_test")
            # seller = seller.seller_user

            items_json = request.POST.get('itemsJson', '')
            mode = request.POST.get('mode', '')
            # print("pickup : ", pickup)
            # delivery = request.POST.get('delivery', '')
            # print("delivery : ", delivery)
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            zip_code = request.POST.get('zip_code', '')
            name = request.user.customer
            amount = request.POST.get('totalPrice_database')
            email = request.user.email
            phone = request.POST.get('inputPhone')
            print("amount : ", amount)
            print("amount : ", type(amount))
            order = Orders(customer=name, items_json=items_json , amount=amount, name=name, email=email, phone=phone, address=address, zip_code=zip_code, mode=mode)
            order.save()



            update = OrderUpdate(customer=name, order_id=order.order_id, update_desc="The order has been placed")
            update.save()
            thank = True
            id = order.order_id                                                     # To get id of the order, that is displayed in alert box and helps to track orders
            messages.success(request, f"Thanks for Ordering. Your order is id {id}. Use this to track your order using order tracker!")
            # ---------------------------------------------------------------------------------------------------
            # sample = f'''{items_json}, {{"id":{id}}}'''
            # filtered = order.objects.values('order_id','items_json')
            # print("filtered")
            # print(filtered)
            
            # file1 = open('myfile.txt', 'w')
            # myData = Orders.objects.values('items_json', 'order_id')
            # string_myData = json.dumps(myData)
            # print("myData : ", myData)
            # file1.write(myData)
            # sample = f'''{items_json}, {{'order_id': {id}}}'''
            sample = f'''{{'order_id': {id}}}'''
            # string_sample = json.dumps(sample)
            sample = sample.replace("\'","\"")
            # AIRTABLE-PYTHON INTEGRATION STARTS
            update_url = env("AIRTABLE_ORDER_UPDATE_URL")
            update_headers = {
                'Authorization': 'Bearer keydq2SURfHCN4Aig',
                'Content-Type': 'application/json'
            }
            update_data = {
                "fields": {
                # "Name": 33,
                "OrderId": sample
            },
            #   "createdTime": "2021-01-02T20:33:49.000Z"
            }
            
            # print(update_data)
            update_response = requests.post(update_url, headers=update_headers, json=update_data)
            # AIRTABLE-PYTHON INTEGRATION ENDS
            
            # file1 = open('myfile.txt','a')
            # file1.write(sample)
            # file1.write("\n")  

            # print("sample :", string_sample)
            big_code = pyqrcode.create(sample, error='L', version=15, mode='binary')
            image_name = id
            image_qrcode = big_code.png(f'media/qrcode/{id}.png', scale=3, module_color=[0, 0, 0], background=[0xff, 0xff, 0xcc])
            order.order_qr = f"media/qrcode/{id}.png"

            cloudinary.config(cloud_name=env("CLOUD_NAME"),api_key=env("API_KEY"), api_secret=env("API_SECRET_CLOUDINARY"))
            cloudinary.uploader.upload(f"media/qrcode/{id}.png",public_id = f'{id}', folder="media/qrcode")



            # qr_photo = Orders.objects.get(order_id=order.order_id)
            # qr_photo.objects.update()
            Orders.objects.filter(order_id=id).update(order_qr=f"media/qrcode/{id}.png")
            
            # Orders.objects.update(
            #     customer=name, items_json=items_json , amount=amount, name=name, email=email, phone=phone, address=address, zip_code=zip_code, mode=mode, order_qr= f"media/qrcode/{id}.png"
            # )


            # qr_photo.order_qr = f"media/qrcode/{id}.png"
            # qr_photo.save()
            # qr_photo, created = Cart.objects.update_or_create(
            #     customer=customer, defaults={"cart_items": data}
            # )
            

            # ---------------------------------------------------------------------------------------------------
            print("imtems_json : ", items_json)

            return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})                    # 'thank' --> new parameter, : thank --> already declared variable
        else:
            # seller = Seller.objects.filter(seller_name="shop_test")
            # seller = seller.seller_user.name
            items_json = request.POST.get('itemsJson', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            amount = request.POST.get('totalPrice_database')
            phone = request.POST.get('inputPhone')
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            zip_code = request.POST.get('zip_code', '')
            mode = request.POST.get('mode', '')

            
            order = Orders(items_json=items_json, amount=amount , name=name, email=email, phone=phone, address=address, zip_code=zip_code, mode=mode)
            order.save()

            update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
            update.save()
            thank = True
            id = order.order_id                                                         # To get id of the order, that is displayed in alert box and helps to track orders
            messages.success(request, f"Thanks for Ordering. Your order is id {id}. Use this to track your order using order tracker!")
            # ---------------------------------------------------------------------------------------------------
            sample = f'''{{'order_id': {id}}}'''
            sample = sample.replace("\'","\"")
            # AIRTABLE-PYTHON INTEGRATION STARTS
            update_url = env("AIRTABLE_ORDER_UPDATE_URL")
            update_headers = {
                'Authorization': 'Bearer keydq2SURfHCN4Aig',
                'Content-Type': 'application/json'
            }
            update_data = {
                "fields": {
                # "Name": 33,
                "OrderId": sample
            },
            #   "createdTime": "2021-01-02T20:33:49.000Z"
            }
            
            # print(update_data)
            update_response = requests.post(update_url, headers=update_headers, json=update_data)
            # AIRTABLE-PYTHON INTEGRATION ENDS
            
            
            # file1 = open('myfile.txt','a')
            # file1.write(sample)         
            # file1.write("\n")          
            big_code = pyqrcode.create(sample, error='L', version=15, mode='binary')
            image_name = id
            image_qrcode = big_code.png(f'media/qrcode/{id}.png', scale=3, module_color=[0, 0, 0], background=[0xff, 0xff, 0xcc])
            order.order_qr = f"media/qrcode/{id}.png"
            cloudinary.config(cloud_name=env("CLOUD_NAME"),api_key=env("API_KEY"), api_secret=env("API_SECRET_CLOUDINARY"))
            cloudinary.uploader.upload(f"media/qrcode/{id}.png",public_id = f'{id}', folder="media/qrcode")
            # ---------------------------------------------------------------------------------------------------
            
            return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})      

    return render(request, 'shop/checkout.html')


def tracker(request):

    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        orderId2 = request.POST.get('emailId', '')
        
        print("orderId : ",orderId)
        print("email : ",orderId2)
        # return HttpResponse(f"{orderId} and {email}")           # Used for testing
        try:
            order = Orders.objects.filter(order_id=orderId, email=orderId2)
            print("order  : ", order)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                print("update", update)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates,order[0].items_json], default=str)
                    print("response : ", response)
                return HttpResponse(response)                                       # Very important to keep this line of code outside the for loop. If indented, it goes inside it, and will only show first update, that is of placing the order.

            else:
                return HttpResponse('{}')

        except Exception as e:
            # return HttpResponse(f'Exeptions  {e}')
            return HttpResponse('{}')



    return render(request, 'shop/tracker.html')




def samplenew(request):
    return render(request, 'shop/samplenew.html')




def handleSignup(request):
    if request.method == 'POST':
        # Get Post Parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorness
        # Username should have less than 10 characters
        if len(username)>20:
            messages.error(request, "Username must be less than 10 characters.")
            return redirect('ShopHome')
        #  Username should be alphanum
        # if not username.isalnum():
        #     messages.error(request, "Username must only contain alphabet or characters.")
        #     return redirect('ShopHome')
        # Passwords should match
        if pass1 != pass2:
            messages.error(request, "Passwords don't match.")
            return redirect('ShopHome')
            
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        # if(request.user=="AnonymousUser"):
        
        #     user_cart = Cart.objects.create(
        #     customer= "AnonymousUser",
        #     cart_items={}
        #     )
        # else:
        #     user_cart = Cart.objects.create(
        #     customer= request.user.customer,
        #     cart_items={})


        # From accounts app
        if username[0:5] == "shop_":
            group = Group.objects.get(name='seller')
            myuser.groups.add(group)
            
            Seller.objects.create(
                seller_user=myuser,
                seller_name=fname,
                seller_email=email,
            )
            messages.success(request, "Your account has been successfully created!")
            return redirect('seller')
        else:
            group = Group.objects.get(name='customer')
            myuser.groups.add(group)
            
            Customer.objects.create(
                user=myuser,
                name=fname,
                email=email,

            )

            messages.success(request, "Your account has been successfully created!")
            return redirect('ShopHome')
    else:
        return HttpResponse("404 - Not Found")  


def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            # if user.groups.filter(name = 'customer').exists():
            
            if loginusername[0:5] == "shop_":
                seller = request.user.seller
                print(seller)
                return redirect('seller')
            else:
                customer = request.user.customer
                print(customer)
                return redirect('ShopHome')



            # try:
            #     some_object
            # except NameError:
            #     do_something()
            # else:
            #     do_something_else()
            # customer_object = Cart.objects.get(customer=customer)
            # customer_cart_item = customer_object.cart_items
            # print(customer_object.cart_items)
            # cart, created = Cart.objects.get_or_create(customer=customer, cart_items=customer_cart_item)

            # return redirect('ShopHome')
        else:
            messages.error(request, "Invalid credentials. Please Try Again.")
            return redirect('ShopHome')


    return HttpResponse("404 - Not Found")






def handleLogout(request):
    logout(request)

    messages.success(request, "Successfully logged out")
    return redirect('ShopHome')


# @api_view(['GET'])
def category(request):
    
    # catprods = Product.objects.filter('category', 'id')
    # cats = {product['category'] for product in allProducts}
    # print(allProducts)
    # print("Now cats")
    # print(cats)
    # context = {'allProducts' : allProducts}

    allProds=[]
    # alldetails = Product.objects.all()
    # contextalldetals = {'alldetails' : alldetails}

    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}                                       # Set comprehension
    print(cats)
    context = {'cats': cats}
    print(context)



    # return Response(context)
    # return render(request, 'shop/category.html', contextalldetals)
    return render(request, 'shop/category.html', context)


    







    # allProds=[]
    # catprods = Product.objects.values('category', 'id')
    # cats = {item['category'] for item in catprods}                                       # Set comprehension
    # for cat in cats:
    #     prod = Product.objects.filter(category=cat)
    #     print(prod)
    #     print("Next loop :")
    #     allProds.append(prod)
        



    # # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
    # # allProds = [[products, range(1, nSlides), nSlides],
    # #             [products, range(1, nSlides), nSlides]]
    # print("Now allProds")
    # print(allProds)
    # params = {'allProds': allProds}
    # # print(params)


def categorySlug(request, slug):
#    print(slug)
   separateProds = []
   catwiseprod = Product.objects.filter(category=slug)
   print(catwiseprod)
   for i in catwiseprod:
    #    print(i.product_name)
    #    print(i.product_id)
       separateProds.append(i)
#    print(separateProds)
   print("Hellow WOrld!")
   if request.user.is_authenticated:
        customer = request.user.customer
        customer_object = Cart.objects.get(customer=customer)
        print(customer_object)
        customer_cart_item = customer_object.cart_items
        print("python object : ", customer_cart_item)
        cart = customer_cart_item.replace("\'", "\"")
        print("replaced : ", cart)
        # cart = json.dumps(customer_cart_item)
        # print("two : ", cart)


        user_cart, created = Cart.objects.get_or_create(customer=customer, cart_items=customer_cart_item)
        params1 = {'separateProds' : separateProds, 'slug' : slug,'user_cart':user_cart, 'cart':cart}
        return render(request, 'shop/categoryslug.html', params1)
   context = {'separateProds' : separateProds, 'slug' : slug}
#    print(context)
   

#    print(catwiseprod)
#    catprods = Product.objects.values('category')
#    print(catprods)

#    for cat in catprods:
#         prod = Product.objects.values(category=cat)
#         print(prod)
#         print("Next loop :")
      
   
   
#    return HttpResponse("CategorySlug : " + slug)
   return render(request, 'shop/categoryslug.html' , context)
    # allProds=[]
    # catprods = Product.objects.values('category','id')
    # cats = {item['category'] for item in catprods}                                       # Set comprehension
    # print(cats)
    # context = {'cats': cats}
    # print(context)
    # for cat in cats:
    #     prod = Product.objects.filter(category=cat)
    #     print(prod)
    #     print("Next loop :")
    #     allProds.append(prod) 
    # print(allProds)
    # context = {'allProds' : allProds} 

def stores(request):
    return render(request, "shop/stores.html")

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    print("data :", data)

    # if request.user == "AnonymousUser":
    #     request.body = {}
    # else:

    # for (item in cart) {

    #   let name = cart[item][1];
    #   let qty = cart[item][0];
    #   let itemPrice = cart[item][2];
    #   sum = sum + qty
    #   totalPrice = totalPrice + qty * itemPrice
    #   mystr = `<li class="list-group-item d-flex justify-content-between align-items-center">
    #                   ${name}
    #                   <span class="badge badge-primary badge-pill">${qty}</span>
    #               </li>`
    #   $('#items').append(mystr);                                                   // could also have used '.innerHTML' of Javascript but instead, chose '.append' function of Jquery


    # }
    sum = 0
    # for item in data:
    #     name = data[item][1]
    #     print("name :", name)
    #     qty = data[item][0]
    #     print("qty :", qty)
    #     price = data[item][2]
    #     print("price :", price)
    #     sum = sum + qty
    print("next item")
    
    # customer_object = Cart.objects.get(customer=customer)
    # customer_cart_item = customer_object.cart_items
    # print(customer_object.cart_items)
    # cart, created = Cart.objects.get_or_create(customer=customer, cart_items=customer_cart_item)



    customer = request.user.customer
    # cart_items = Cart.objects.create(cart_items=data)
    # cart, created = Cart.objects.get_or_create(customer=customer, cart_items=data)
    cart, created = Cart.objects.update_or_create(
        customer=customer, defaults={"cart_items": data}
    )
        

    # name = data['name']
    # price = data['price']

    # print('Quantity: ', qty)
    # print('name: ', name)
    # print('price: ', price)
    return JsonResponse('item was added', safe=False)

def qrcode(request, order_id):
    order = Orders.objects.get(order_id=order_id)
    print("order Amount : ", order.amount)
    context = {'order_id':order_id, 'order':order}

    return render(request, 'shop/qrcode.html', context)


@api_view(['GET'])
def allOrders(request):
    all_orders = Orders.objects.all()
    print("type :: ", type(all_orders))
    print("type :: ", all_orders)
    serializer = AllOrdersSerializer(all_orders, many=True)
    # print("All Orders : ", all_orders)

    return Response(serializer)