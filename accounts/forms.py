from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError 
from .models import CustomUser

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2',)
        