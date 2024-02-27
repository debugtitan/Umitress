from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'address', 'state', 'city','mobile']
        # exclude = ('customer',)

        widgets = {
            'first_name':forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
            'state':forms.TextInput(attrs={'class': 'form-control'}),
            'city':forms.TextInput(attrs={'class': 'form-control'}),
            'mobile':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'+234'}),
       


        }