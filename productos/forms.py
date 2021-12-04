from django import forms
from .models import Price_product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class price_product_form(forms.ModelForm):

    class Meta:
        model = Price_product
        fields = '__all__'



class customerRegisterForm(UserCreationForm):
    pass


