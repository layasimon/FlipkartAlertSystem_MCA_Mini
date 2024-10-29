from django.urls import path
from.import views
urlpatterns = [
    path("", views.indexview, name="index"),
    path("Register/", views.registerview, name="register"),
    path("login/", views.loginview, name="login"),
    path("home/", views.homeview, name="home"),
    path("logout/",views.logoutview,name="logout"),
    path('add/', views.add_to_watchlist, name='add_to_watchlist'),
    path("watchlist/",views.watchlistview,name="watchlist"),
    path('history/',views.watchlist_historyview, name='watchlist_history'),
    path('confirm_update/', views.confirm_update, name='confirm_update'),
]