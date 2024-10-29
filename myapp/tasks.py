
# myapp/tasks.py

from celery import shared_task
from django.contrib.auth.models import User
from .models import WatchlistItem, WatchlistHistory
from django.utils.timezone import localtime
from .utils import get_product_id_from_url, fetch_product_details, send_email

@shared_task
def compare_price_and_notify(product_url, trigger_price, user_email, user_id):
    """Compare price, notify user, and manage watchlist/history."""
    pid = get_product_id_from_url(product_url)
    if not pid:
        return False  # No valid product ID

    product_title, current_price = fetch_product_details(pid)

    try:
        current_price = float(current_price)
        trigger_price = float(trigger_price)
    except (ValueError, TypeError):
        return False  # Invalid price data

    if current_price <= trigger_price:
        # Send notification email
        send_email(product_title, current_price, product_url, user_email)

        # Save product details to WatchlistHistory before deleting
        WatchlistHistory.objects.create(
            user_id=user_id,
            product_url=product_url,
            product_title=product_title,
            price_at_notification=current_price,
            email=user_email,
            date_notified=localtime()
        )

        # Delete the product from WatchlistItem
        WatchlistItem.objects.filter(
            user_id=user_id, product_url=product_url
        ).delete()

        return 'email_sent'
