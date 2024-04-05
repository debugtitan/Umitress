from django.urls import path
from .import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='store'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_categories'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('updateItem', views.updateItem, name='update_item'),


]
