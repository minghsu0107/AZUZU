from django import forms
from .models import Order

class ContactForm(forms.Form):
	contact_email = forms.EmailField(max_length=200)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('items', 'name', 'email', 'address', 'city', 'state', 'zipcode', 'total')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'John'}),
            'email': forms.EmailInput(attrs={'placeholder': 'john@example.com'}),
            'address': forms.TextInput(attrs={'placeholder': '1234 Main St.'}),
            'city': forms.TextInput(attrs={'placeholder': ''}),
            'state': forms.TextInput(attrs={'placeholder': ''}),
            'zipcode': forms.TextInput(attrs={'placeholder': ''}),
        }
