from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json 
import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from ecommerce import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import *

# Create your views here.
def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    #validations
        if form.is_valid():
            my_user=User.objects.create_user(form.cleaned_data.get("username"),form.cleaned_data.get("email"),form.cleaned_data.get("password1"))
            my_user.save()
            cust = Customer.objects.create(user=my_user,name=my_user.username,email=my_user.email)
            cust.save()
            login(request, my_user)
            messages.success(request, "Your Account has been successfully created.") 
            # Welcome Email
            subject = "Welcome to Aybo Lanka Login!!"
            message = "Hello " + my_user.username + "!! \n" + "Welcome to Aybo Lanka!! \nThank you for visiting our website.\nHope you Enjoy our website.\n\nThanking You"        
            from_email = settings.EMAIL_HOST_USER
            to_list = [my_user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)    
            return redirect("home")

    return render(request,"store/signup.html", {"form": form})

def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password1=request.POST.get('password')
        user=authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return  render(request, 'store/login.html')

def signout(request):
    logout(request)
    return redirect("signup")

def home(request):
 place = Places.objects.all()
 context = {'place':place,}

 return render(request,"store/home.html",context)

# def home(request):

#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)                
#         items = order.orderitem_set.all()
#         print(items)       
#         cartItems = order.get_cart_items
#     else: 
#         items = []              
#         order = {'get_cart_total':0, 'get_cart_items':0, 'Shipping':False} 
#         cartItems = order['get_cart_items']  
       

#     place = Places.objects.all()
#     context = {'products':products, 'cartItems':cartItems}
#     return render(request, 'store/store.html', context)








def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)                
        items = order.orderitem_set.all()
        print(items)       
        cartItems = order.get_cart_items
    else: 
        items = []              
        order = {'get_cart_total':0, 'get_cart_items':0, 'Shipping':False} 
        cartItems = order['get_cart_items']  
       

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

 
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)   
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        print(created) 
    else:
        
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'Shipping':False}
        cartItems = order['get_cart_items']

    context = {'items' :items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

#  if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)   
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#         print(created) 
#     else:
        
#         items = []
#         order = {'get_cart_total':0, 'get_cart_items':0, 'Shipping':False}
#         cartItems = order['get_cart_items']

#     context = {'items' :items, 'order':order, 'cartItems':cartItems}
#     return render(request, 'store/cart.html', context)



def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        print(order.orderitem_set.all())
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'Shipping':False}
        cartItems = order['get_cart_items']
     
    context = {'items' :items, 'order':order, 'cartItems':cartItems}   
    return render(request, 'store/checkout.html', context) 
       
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    customer.cart.add(product)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
   

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False) 


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder (request): 
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id =  transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()   

        if order.shipping == True:
           shippingAddress.objects.create(
               customer = customer,
               order = order,
               address = data['shipping']['address'],
               city = data['shipping']['city'],
               state = data['shipping']['state'],
               zipcode = data['shipping']['zipcode'],               
            ) 

    else:
        print('User is not logged in..')        

    return JsonResponse('Payment completed !', safe=False) 
