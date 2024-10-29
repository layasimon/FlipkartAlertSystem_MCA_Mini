from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Profile model for user bio
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# Model for login details
class LoginUser(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)


# Model for users who track products
class HomeUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_url = models.URLField(max_length=200, primary_key=True)
    trigger_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    email = models.EmailField(max_length=200, unique=True)


class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_url = models.URLField(max_length=200)
    product_title = models.CharField(max_length=255)  # New field for product title
    trigger_price = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(max_length=100)
    cu_id = models.AutoField(primary_key=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_title} - ₹{self.trigger_price}"



class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who added the item
    product_url = models.URLField(max_length=500)  # Product URL
    title=models.CharField(max_length=200)
    trigger_price = models.DecimalField(max_digits=10, decimal_places=2)  # Target price
    email = models.EmailField()  # User's email for notifications
    date_added = models.DateTimeField(default=now)  # Timestamp of when the item was added

    def __str__(self):
        return f"{self.user.username} - {self.product_url}"
    
class WatchlistHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_url = models.URLField()
    product_title = models.CharField(max_length=255)
    price_at_notification = models.FloatField()
    email = models.EmailField()
    date_notified = models.DateTimeField(default=now)

    def __str__(self):
        return f"History: {self.product_title} - {self.user.username}"

