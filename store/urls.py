from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.signin,name="login"),
    path('logout/',views.signout,name="logout"),
    path('home/',views.home,name="home"),
    path('',views.home,name="home"),
    path('store/',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    

    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),
    




]