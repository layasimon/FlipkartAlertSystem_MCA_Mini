
import requests
from urllib.parse import urlparse, parse_qs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from .models import WatchlistItem
# from django.utils.timezone import localtime

def get_product_id_from_url(product_url):
    """Extract the product ID (pid) from the given Flipkart product URL."""
    parsed_url = urlparse(product_url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("pid", [None])[0]

def fetch_product_details(pid):
    """Fetch product details from Flipkart API."""
    url = "https://real-time-flipkart-api.p.rapidapi.com/product-details"
    querystring = {"pid": pid}

    headers = {
        "x-rapidapi-key": "85d56b1438mshb768ff826a519efp1a3ee3jsnff41b9f1a079",
        "x-rapidapi-host": "real-time-flipkart-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        product_details = response.json()
        title = product_details.get('title', 'N/A')
        price = product_details.get('price', 'N/A')
        if isinstance(price, dict):
            price = price.get('amount', 'N/A')
        return title, price
    else:
        return None, None



def send_email(title, price, product_url, receiver_email):
    """Send an email with product details, including the product URL."""
    sender_email = "projectm571@gmail.com"
    password = "dtexasgbahfaepcm"

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Product Price Alert"

    # Email body with product details
    message_body = (
        f"Product Title: {title}\n"
        f"Price: ₹{price}\n"
        f"Product URL: {product_url}"
    )
    message.attach(MIMEText(message_body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Error: {e}")


# def compare_price_and_notify(product_url, trigger_price, user_email, user):
#     """Compare price and handle notification or storage."""
#     pid = get_product_id_from_url(product_url)
#     if not pid:
#         return False  # No valid product ID

#     product_title, current_price = fetch_product_details(pid)

#     try:
#         # Ensure prices are valid floats for comparison
#         current_price = float(current_price)
#         trigger_price = float(trigger_price)
#     except (ValueError, TypeError):
#         return False  # Invalid price data

#     if current_price <= trigger_price:
#         # Send notification email
#         send_email(product_title, current_price, product_url, user_email)
#         return 'email_sent'
#     else:
#         # Store product details in the WatchlistItem model
#         WatchlistItem.objects.create(
#             user=user,
#             product_url=product_url,
#             product_title=product_title,  # Save the product title
#             trigger_price=trigger_price,
#             email=user_email,
#             date_added=localtime()  # Store current time
#         )
#         return 'saved'
