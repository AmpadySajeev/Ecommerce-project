from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from ecom.models import Shoes, ShoeImage

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'name')
    
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'name', 'is_active', 'is_staff'
        )

class ShoeForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = [
            'name','brand','image','description','price','category','is_featured'
        ]

class ShoeImageForm(forms.ModelForm):
    class Meta:
        model = ShoeImage
        fields = ['image']