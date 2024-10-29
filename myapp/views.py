from django.shortcuts import render, redirect
from . forms import RegisterForm
from . forms import LoginForm
from . forms import HomeForm
from . forms import WatchlistItemForm#,WatchlistForm
from . models import WatchlistItem,WatchlistHistory
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .tasks import compare_price_and_notify
from .helper import save_in_watchlist

from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.

def indexview(request):
    return render(request, "index.html")


def registerview(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
        else:
            return render(request, "register.html", {'form': form})
    else:
        form = RegisterForm()
        return render(request, "register.html", {'form': form})

def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            if form.is_valid():
                form.save()
                return redirect('home')   
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('home')
    else:
        return render(request, "login.html", {'form': LoginForm()}) 


def logoutview(request):
    return redirect('index')


    
def homeview(request):
    if request.method=='POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form=HomeForm()
        return render(request, "home.html", {'form':form})
    
# @login_required
# def add_to_watchlist(request):
#     """Handle adding a product to the watchlist asynchronously."""
#     if request.method == 'POST':
#         form = WatchlistItemForm(request.POST)
#         if form.is_valid():
#             product_url = form.cleaned_data['product_url']
#             trigger_price = form.cleaned_data['trigger_price']
#             user_email = form.cleaned_data['email']
#             user_id = request.user.id  # Pass user ID to the Celery task
#             save_in_watchlist(product_url, trigger_price, user_email, user_id)
#             # Trigger Celery task asynchronously
#             compare_price_and_notify.delay(
#                 product_url, trigger_price, user_email, user_id
#             )

#             messages.info(request, 'Processing your request in the background.')
#             return redirect('home')  # Redirect after form submission

#     else:
#         form = WatchlistItemForm()

#     return render(request, 'add_to_watchlist.html', {'form': form})


def add_to_watchlist(request):
    if request.method == "POST":
        form = WatchlistItemForm(request.POST)
        if form.is_valid():
            product_url = form.cleaned_data['product_url']
            trigger_price = form.cleaned_data['trigger_price']

            # Create the WatchlistItem
            watchlist_item = WatchlistItem.objects.create(
                user=request.user,
                product_url=product_url,
                trigger_price=trigger_price
            )
            messages.success(request, "Product added to the watchlist.")

            # Make sure to pass the required parameters correctly
            compare_price_and_notify.delay(
                product_url, 
                trigger_price, 
                request.user.email,  # Use request.user's email
                request.user.id      # Use request.user's ID
            )
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = WatchlistItemForm()

    return render(request, 'add_to_watchlist.html', {'form': form})





@login_required
def watchlistview(request):
    """Display the products in the user's watchlist."""
    watchlist_items = WatchlistItem.objects.filter(user=request.user)
    return render(request, 'watchlist.html', {'watchlist': watchlist_items})



def confirm_update(request):
    if request.method == "POST" and request.POST.get('confirm') == "yes":
        product_url = request.POST.get('product_url')
        new_trigger_price = request.POST.get('trigger_price')

        # Update the trigger price
        existing_entry = get_object_or_404(WatchlistItem, product_url=product_url)
        existing_entry.trigger_price = new_trigger_price
        existing_entry.save()

        messages.success(request, 'Trigger price updated successfully.')
        return redirect('watchlist')

    messages.info(request, 'Update canceled.')
    return redirect('add_to_watchlist')







@login_required
def watchlist_historyview(request):
    """Display the user's watchlist history."""
    history_items = WatchlistHistory.objects.filter(user=request.user)
    return render(request, 'watchlist_history.html', {'history': history_items})

