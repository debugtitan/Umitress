from django.shortcuts import render
from .models import Order, OrderItem

def verify_pay(request, ref):
    payment = Order.objects.get(ref=ref)
    verified = payment.verify_payment()
  

    if verified:     
        customer = request.user
        order = Order.objects.get(customer=customer, verified=True, ref=ref)
        orderItem = OrderItem(order=order)
        orderItem.delete
        # order = {'get_cart_total':0, 'count_cart':0}
    return render(request, 'cart/thankyou.html')
    
  
    
