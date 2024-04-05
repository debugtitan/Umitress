import secrets
from django.db import models
from accounts.models import CustomUser
from store.models import Product
from .paystack import PayStack



class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    ref = models.CharField(max_length=200)
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Order.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
   
        super().save(*args, **kwargs)
        
    @property
    def amount_value(self):
        return int(self.get_cart_total) * 100

    def verify_payment(self):
        amount = int(self.get_cart_total)
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref,  amount)
        if status:
            if result['amount'] / 100 == amount:
                self.verified = True
                self.save()
        if self.verified:
            return True
        return False

    def __str__(self):
        return f'Order {str(self.id)} for {self.customer}' 
    
    @property
    def get_cart_total(self):
        orderitems = self.order_items.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def count_cart(self):
        orderitems = self.order_items.all()
        total = sum([item.quantity for item in orderitems])
        return total


    def getCustomerEmail(self):
        return self.customer



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items", null=True)
    quantity = models.PositiveIntegerField(default=0, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} {self.product.name}'  
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
    def getCustomerEmail(self):
        return self.customer
    
 