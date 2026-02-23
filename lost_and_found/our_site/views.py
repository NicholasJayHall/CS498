from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import LostItem, EmailSubscription
from .forms import LostItemForm, EmailSubscriptionForm, UserRegisterForm


def home(request):
    """Landing page – hero + recent items."""
    recent_items = LostItem.objects.filter(status='lost').order_by('-created_at')[:6]
    subscribe_form = EmailSubscriptionForm()
    return render(request, 'our_site/home.html', {
        'recent_items': recent_items,
        'subscribe_form': subscribe_form,
    })


def item_list(request):
    """Browsable, filterable grid of all lost items."""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    status_filter = request.GET.get('status', 'lost').strip()

    items = LostItem.objects.all()

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    if category:
        items = items.filter(category=category)
    if status_filter and status_filter != 'all':
        items = items.filter(status=status_filter)

    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = LostItem.CATEGORY_CHOICES

    return render(request, 'our_site/item_list.html', {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'status_filter': status_filter,
        'categories': categories,
        'total_count': items.count(),
    })


def item_detail(request, pk):
    """Full item detail + email subscription form."""
    item = get_object_or_404(LostItem, pk=pk)
    subscribe_form = EmailSubscriptionForm()

    if request.method == 'POST':
        subscribe_form = EmailSubscriptionForm(request.POST)
        if subscribe_form.is_valid():
            email = subscribe_form.cleaned_data['email']
            sub, created = EmailSubscription.objects.get_or_create(email=email)
            if not sub.active:
                sub.active = True
                sub.save()
            if created:
                messages.success(request, f'✅ You\'ll be notified at {email} when new items are reported.')
            else:
                messages.info(request, f'📬 {email} is already subscribed to notifications.')
            return redirect('item_detail', pk=pk)

    return render(request, 'our_site/item_detail.html', {
        'item': item,
        'subscribe_form': subscribe_form,
    })


@login_required
def report_item(request):
    """Form to report a new lost or found item."""
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.reporter = request.user
            if not item.contact_email:
                item.contact_email = request.user.email
            item.save()
            messages.success(request, f'📋 "{item.title}" has been posted successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = LostItemForm(initial={'contact_email': request.user.email})

    return render(request, 'our_site/report_item.html', {'form': form})


@login_required
def mark_found(request, pk):
    """Toggle item status between lost and found."""
    item = get_object_or_404(LostItem, pk=pk)
    if request.user == item.reporter or request.user.is_staff:
        if item.status == 'lost':
            item.status = 'found'
            messages.success(request, f'🎉 "{item.title}" has been marked as found/claimed!')
        else:
            item.status = 'lost'
            messages.info(request, f'"{item.title}" has been marked as still lost.')
        item.save()
    else:
        messages.error(request, 'You do not have permission to update this item.')
    return redirect('item_detail', pk=pk)


@login_required
def delete_item(request, pk):
    """Delete a lost item (owner or staff only)."""
    item = get_object_or_404(LostItem, pk=pk)
    if request.user == item.reporter or request.user.is_staff:
        if request.method == 'POST':
            title = item.title
            item.delete()
            messages.success(request, f'🗑️ "{title}" has been deleted.')
            return redirect('item_list')
    else:
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('item_detail', pk=pk)
    return render(request, 'our_site/confirm_delete.html', {'item': item})


def register(request):
    """User registration page."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎓 Welcome, {user.first_name}! Your account has been created.')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'our_site/register.html', {'form': form})


def login_view(request):
    """Login page."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'👋 Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'our_site/login.html', {'form': form})


def logout_view(request):
    """Logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def subscribe_email(request):
    """Standalone subscribe page."""
    if request.method == 'POST':
        form = EmailSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            sub, created = EmailSubscription.objects.get_or_create(email=email)
            if not sub.active:
                sub.active = True
                sub.save()
            if created:
                messages.success(request, f'✅ Subscribed! You\'ll receive alerts at {email}.')
            else:
                messages.info(request, f'📬 {email} is already subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def unsubscribe(request, email):
    """Unsubscribe link sent in emails."""
    try:
        sub = EmailSubscription.objects.get(email=email)
        sub.active = False
        sub.save()
        messages.success(request, f'You have been unsubscribed from notifications.')
    except EmailSubscription.DoesNotExist:
        messages.error(request, 'Subscription not found.')
    return render(request, 'our_site/unsubscribed.html', {'email': email})
