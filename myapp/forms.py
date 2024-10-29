from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LoginUser, HomeUser, WatchlistItem,Watchlist
from .utils import fetch_product_details  # Import the utility function

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginUser
        fields = ['username', 'password', 'email']

class HomeForm(forms.ModelForm):
    class Meta:
        model = HomeUser
        fields = ['product_url', 'trigger_price', 'email']

    def clean_product_url(self):
        product_url = self.cleaned_data.get('product_url')
        details = fetch_product_details(product_url)
        if 'error' in details:
            raise forms.ValidationError(details['error'])
        return product_url

class WatchlistItemForm(forms.ModelForm):
    class Meta:
        model = WatchlistItem
        fields = ['product_url', 'trigger_price', 'email', 'cu_id']
        widgets = {
            'trigger_price': forms.NumberInput(attrs={'step': '0.01'}),
        }


class WatchlistForm(forms.ModelForm):
    class Meta:
        model=Watchlist
        fields=['user','product_url','title','trigger_price','email','date_added']
