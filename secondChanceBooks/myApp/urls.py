from django.contrib import admin
from django.urls import path,include
from myApp import views

urlpatterns = [
    path('', views.index, name = "Home"),
    path('login', views.loginUser, name = "Login"),
    path('logout', views.logoutUser, name = "Logout"),
    path('signup', views.signupUser, name = "SignUp"),
    path('searchProd', views.searchProd, name = "SearchProd"),
    path('bookview/sellbook',views.sellbook, name="Sellbook"),
    path('bookview/profile',views.profile, name="Profile"),
    path('bookview/login',views.loginUser, name = "login"),
    path('bookview/logout',views.logoutUser, name = "logout"),
    path('bookview/cart', views.cart, name="Cart"),
    path('bookview/update_item/', views.updateItem, name = 'update_item'),
    path('bookview/save-shipping-address/', views.save_shipping_address, name='Save-Shipping-Address'),
    path('bookview/<str:bookname>',views.bookview, name="BookView"),
    path('sellbook', views.sellbook, name = "SellBook"),
    path('profile', views.profile, name="profile"),
    path('cover', views.cover, name="cover"),
    path('cart', views.cart, name="cart"),
    path('update_item/', views.updateItem, name='updateItem'),
    path('save-shipping-address/', views.save_shipping_address, name='save-shipping-address')
]