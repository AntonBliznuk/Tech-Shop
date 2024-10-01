from django import forms

class OrderForm(forms.Form):
    user_phone = forms.IntegerField()