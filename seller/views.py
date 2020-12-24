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

# import cv2
# import numpy as np
# import urllib.request
# from pyzbar.pyzbar import decode


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




def qrcode(request):
    # url = pyqrcode.create('http://uca.edu')
    # svg = url.svg('uca-url.svg', scale=8)
    # print(url.terminal(quiet_zone=1))
    
    
    # orders = Orders.objects.values('items_json', 'order_id')
    # cats = {item['order_id'] for item in orders}                                       # Set comprehension
    # print(orders)
    # print("NEXT")
    # print(cats)

    file1 = open('myfile.txt', 'a')
    myData = Orders.objects.values('order_id').all()
    # myData2 = Orders.objects.filter(order_id=myData)
    print("before - myData : ", myData)
    for i in myData:
        i_string = json.dumps(i)
        print(i_string)
        file1.write(i_string)
        file1.write("\n")

    # string_myData = json.dumps(myData)
    # string_myData = string_myData.replace("\\"," ")
    # print(type(string_myData))
    # print("myData : ", myData)
    # print("NEXT")
    # file1.write(string_myData)
    # file1.write("\n")
    # for cat in cats:
    #     prod = Orders.objects.filter(order_id=cat)
    #     print("prod : ", prod)
    # --------------------------------------------------------------------------------------------------------------------
    # text = '''"{"pr48":[3,"Dettol Original Germ Protection Bathing Soap bar,",200],"pr47":[2,"Horlicks Health and Nutrition drink - 1 kg Pet Jar",445],"pr12":[2,"Maggi",45],"pr23":[2,"Gits Ready to Eat Dal Makhani, 300g",99],"pr45":[2,"Savlon Glycerine Soap, 125g (Buy 3 Get 1 Free)",144],"pr46":[2,"Bournvita Health Drink Jar, 1 kg",360],"pr16":[2,"he Subtle Art of Not Giving a F*Ck - A Counterintu",266]}"'''
    # big_code = pyqrcode.create(f'''{text}''', error='L', version=15, mode='binary')
    # image_name = 'code1'
    # image_qrcode = big_code.png(f'media/qrcode/{image_name}.png', scale=3, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])

    # context = {'image_name':image_name, 'image_qrcode':image_qrcode}
    return HttpResponse("qrcode!")


def scanqr(request):
    # # img = cv2.imread('image.PNG')

    # url = 'http://192.168.43.8/cam-lo.jpg'
    # cv2.namedWindow("window", cv2.WINDOW_AUTOSIZE)

    # with open('myfile.txt') as f:
    #     myDataList = f.read().splitlines()
    # print(myDataList)

    # while True:
    #     imgResponse = urllib.request.urlopen(url)
    #     imgnp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
    #     # print("imgnp  :  ",imgnp)
    #     img = cv2.imdecode(imgnp, -1)
    #     # print("img : ", img)
    #     for qrcode in decode(img):
    #         # print(qrcode.data)
    #         myData = qrcode.data.decode('utf-8')
    #         print("mydata : ", myData)
    #         file1 = open('sample.txt','a')
    #         file1.write(myData)
    #         pts = np.array([qrcode.polygon],np.int32)
    #         pts = pts.reshape((-1,1,2))
    #         cv2.polylines(img,[pts],True,(204,102,0),5)

    #         pts2 = qrcode.rect
    #         cv2.putText(img,myData,(pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9,(204,102,0),2)
    #     # gray = cv2.cvtColor(img, cv2.COLOR_BayerBG2GRAY)

    #     cv2.imshow("window", img)
    #     key = cv2.waitKey(5)
    #     if key == ord('q'):
    #         break

    # cv2.destroyAllWindows


    return HttpResponse("ScanQr")




