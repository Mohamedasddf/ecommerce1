from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product1/', views.product1, name='product1'),
    path('product1/<int:pk>/', views.product_detail, name='product1'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search_view, name='search'),
    path('search_results/', views.search_results, name='search_results'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('product_favorites/<int:pk>/', views.product_favorites, name='product_favorites'),
    path('show_product_favorites/', views.show_product_favorites, name='show_product_favorites'),
    path('cart/', views.cart, name='cart'),
    path('update_cart_quantity/<int:pk>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('payment/',views.payment, name='payment'),
    path('paypal-payment-success/', views.paypal_webhook, name='paypal-payment-success'),
    path('payment-success/', views.payment_success, name='payment_success'),  # رابط النجاح
    path('payment-failure/', views.payment_failure, name='payment_failure'),  # رابط الفشل

] 
