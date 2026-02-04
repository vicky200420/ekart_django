from django.contrib import admin
from django.urls import path
from .views import*

urlpatterns = [
    path('',home,name="home"),
    path('register',register,name="register"),
    path('login',login_page,name="login"),
    path('logout',logout_page,name="logout"),
    path('cart',cart_pages,name='cart'),
    path('delete/<str:cid>',remove_cart,name='delete'),
    path('fav',fav_pages,name='fav'),
    path('delete_fav/<str:fid>',delete_fav,name='delete_fav'),
    path('favviewpage',favviewpage,name='favviewpage'),
    path('collection',collection,name='collection'),
    path('collections/<str:name>',collectionview,name='collection'),
    path('collections/<str:cname>/<str:pname>',product_details,name='product_details'),
    path('addtocard',addtocard,name='addtocard'),
    path('place-order/',place_order, name='place_order'),
    path('my-orders/', my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/',cancel_order, name='cancel_order'),


]