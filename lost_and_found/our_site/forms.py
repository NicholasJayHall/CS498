from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import LostItem, EmailSubscription


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required – used for notifications.')
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LostItemForm(forms.ModelForm):
    date_lost = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Date Lost/Found'
    )

    class Meta:
        model = LostItem
        fields = ['title', 'description', 'category', 'location', 'date_lost', 'image', 'contact_email', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Blue North Face Backpack'}),
            'description': forms.Textarea(attrs={
                'rows': 4, 'class': 'form-control',
                'placeholder': 'Describe the item – color, brand, any distinguishing marks…'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Student Center, Room 205'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.edu'
            }),
        }
        labels = {
            'status': 'Item Status',
            'contact_email': 'Your Contact Email',
        }


class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.edu'
            })
        }
        labels = {
            'email': 'Email Address'
        }
