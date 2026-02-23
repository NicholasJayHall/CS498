from django.contrib import admin
from .models import LostItem, EmailSubscription


@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'location', 'date_lost', 'reporter', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'location', 'contact_email')
    list_editable = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('email',)
    list_editable = ('active',)
