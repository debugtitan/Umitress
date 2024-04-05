from django.urls import path
from .views import verify_pay

app_name = 'order'

urlpatterns = [
    path('verify_pay/<str:ref>/', verify_pay, name='verify-pay')
]
