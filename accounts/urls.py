from django.urls import path
from .views import login_page, logoutUser, signUp

app_name = 'account'

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logoutUser, name='log-out'),
    path('signup/', signUp, name='sign-up'),
]
