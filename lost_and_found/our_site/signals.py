from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from .models import LostItem, EmailSubscription


@receiver(post_save, sender=LostItem)
def notify_subscribers_on_new_item(sender, instance, created, **kwargs):
    """
    When a new LostItem is created, email all active subscribers.
    """
    if not created:
        return  # Only notify on new posts, not updates

    subscribers = EmailSubscription.objects.filter(active=True)
    if not subscribers.exists():
        return

    subject = f'🔍 New Lost Item Posted: {instance.title}'

    for subscription in subscribers:
        unsubscribe_url = f'/unsubscribe/{subscription.email}/'
        context = {
            'item': instance,
            'unsubscribe_url': unsubscribe_url,
            'site_name': 'Campus Lost & Found',
        }
        html_message = render_to_string('our_site/email/new_item_notification.html', context)
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.email],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception as e:
            print(f'[LostFound] Failed to send email to {subscription.email}: {e}')
