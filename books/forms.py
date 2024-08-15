from django import forms

class PaymentForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class RentBookForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    # Add other fields if necessary