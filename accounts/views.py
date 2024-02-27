from django.shortcuts import redirect, render
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserForm

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('store:store')


    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)

        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist!!')

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:store')
        else:
            messages.error(request, "Invalid Credentails!!")
          
          

    return render(request, 'account/log-in.html',{'page':page})



def logoutUser(request):
        logout(request)
        return redirect('account:login')
    
def signUp(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User has been created")
            return redirect('account:login')
        else:
            messages.error(request, 'Opss!!, An error ocurred, please check your credentials  again!')
           
    return render(request, 'account/sign-up.html', {'form':form})
