from datetime import date
from django.core.exceptions import ValidationError
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

    # Ensure the email is a valid UKY email address
    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if email and not email.endswith('@uky.edu'):
            raise ValidationError("Please use your @uky.edu email address to register.")
        return email


class LostItemForm(forms.ModelForm):
    date_lost = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Date Found'
    )

    class Meta:
        model = LostItem
        fields = ['title', 'description', 'category', 'location', 'date_lost', 'image', 'contact_email']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Blue North Face Backpack'}),
            'description': forms.Textarea(attrs={
                'rows': 4, 'class': 'form-control',
                'placeholder': 'Describe the item – color, brand, any distinguishing marks…'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Student Center, Room 205'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@uky.edu'
            }),
        }
        labels = {
            'contact_email': 'Your Contact Email',
        } 

    def clean_date_lost(self):
        date_lost = self.cleaned_data.get('date_lost')
        # Check if the date is in the future
        if date_lost and date_lost > date.today():
            raise ValidationError("The date lost or found cannot be in the future.")
        return date_lost


class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@uky.edu'
            })
        }
        labels = {
            'email': 'Email Address'
        }
    # Ensure the email is a valid UKY email address
    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if email and not email.endswith('@uky.edu'):
            raise ValidationError("Please use your @uky.edu email address to subscribe.")
        return email