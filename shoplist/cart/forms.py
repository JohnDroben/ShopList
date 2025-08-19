from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=200, label="Имя")
    email = forms.EmailField(label="Email")
    address = forms.CharField(widget=forms.Textarea, label="Адрес")