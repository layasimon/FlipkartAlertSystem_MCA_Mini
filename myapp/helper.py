
# myapp/helper.py


from django.contrib.auth.models import User
from .models import WatchlistItem
from django.utils.timezone import localtime
from .utils import get_product_id_from_url, fetch_product_details


def save_in_watchlist(product_url, trigger_price, user_email, user_id):
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

    if current_price > trigger_price:
        # Store product in the watchlist if the price condition is not met
        user = User.objects.get(pk=user_id)
        WatchlistItem.objects.update_or_create(
            user=user,
            product_url=product_url,
            defaults={
                'product_title': product_title,
                'trigger_price': trigger_price,
                'email': user_email,
                'date_added': localtime(),
            }
        )
        return 'saved'
