from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from Order.models import Order, OrderItem
import json
from django.core.exceptions import MultipleObjectsReturned
from Order.forms import ShippingAddressForm
from django.contrib import messages
from django.conf import settings
import time

def product_list(request, category_slug=None):
    user = request.user
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        print('category slug: ',category_slug)
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
       
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, verified=False)
        items = order.order_items.all()
        cartItems = order.count_cart
        
    else:
        items = []
        order = {'get_cart_total':0, 'count_cart':0}
        cartItems = order['count_cart']

    context ={
        'category':category,
        'categories':categories,
        'products': products,
        'cartItems': cartItems,
        'user': user
        
        
    }

    return render(request, 'store/shop.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, verified=False)
        items = order.order_items.all()
        mail = order.getCustomerEmail
    
        
    else:
        items = []
        order = {'get_cart_total':0, 'count_cart':0}
        
 
    context = {'items':items, 'order':order}
    return render(request, 'cart/cart.html', context)


def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, verified=False)
        items = order.order_items.all()
        
        
    else:
        items = []
        order = {'get_cart_total':0, 'count_cart':0}

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.customer = customer
            shipping_address.order = order
            shipping_address.save()
            print(shipping_address)
            return render(request, 'cart/cart_payment.html', {'order':order, 'paystack_key':settings.PAYSTACK_PUBLIC_KEY})
    else:
        form = ShippingAddressForm()
    context = {'items':items, 'order':order, 'form':form}
    return render(request, 'cart/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('ID:', productId, 'Action:', action)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, verified=False)
    # order = Order.objects.create(customer=customer, verified=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    # orderItem = OrderItem.objects.create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False) 

