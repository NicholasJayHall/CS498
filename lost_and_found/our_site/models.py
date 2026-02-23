from django.db import models
from django.contrib.auth.models import User


class LostItem(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing & Accessories'),
        ('keys', 'Keys'),
        ('wallet', 'Wallet & IDs'),
        ('backpack', 'Backpack & Bags'),
        ('jewelry', 'Jewelry'),
        ('books', 'Books & Notes'),
        ('sports', 'Sports Equipment'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found / Claimed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    location = models.CharField(max_length=200, help_text='Where was it lost/found?')
    date_lost = models.DateField(help_text='Date item was lost or found')
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_items')
    contact_email = models.EmailField(help_text='Email address people can reach you at')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lost')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_status_display()}] {self.title}'


class EmailSubscription(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email} ({"active" if self.active else "inactive"})'
