from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    """Model to store preset drop-off and find locations."""
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField()
    location = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


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
        ('found', 'Claimed'),
    ]

    STORAGE_CHOICES = [
        ('REPORTER', 'I have it with me'),
        ('SITE', 'I left it where I found it'),
        ('DROPOFF', 'I left it at a drop-off location'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    found_location = models.CharField(max_length=200, null=True, blank=True)
    storage_status = models.CharField(max_length=10,choices=STORAGE_CHOICES,default='SITE')
    drop_off_location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Where is this item or where was it left?'
    )
    date_lost = models.DateField(help_text='Date item was lost or found')
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_items')
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
