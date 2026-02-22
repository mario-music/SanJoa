from django.urls import path
from . import views

app_name = 'botanical'

urlpatterns = [
    # Page Views
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('plant-doctor/', views.plant_doctor, name='plant_doctor'),
    path('join-us/', views.join_us, name='join_us'),
    path('about-us/', views.about_us, name='about_us'),
    path('membership/', views.membership, name='membership'),
    path('membership/upgrade/<int:plan_id>/', views.upgrade_membership, name='upgrade_membership'),
    path('orders/', views.orders, name='orders'),
    path('sales/', views.sales, name='sales'),
    path('account/', views.account, name='account'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # API Endpoints
    path('api/products/', views.api_products, name='api_products'),
    path('api/wishlist/toggle/', views.api_wishlist_toggle, name='api_wishlist_toggle'),
    path('api/cart/add/', views.api_cart_add, name='api_cart_add'),
    path('api/diagnose-plant/', views.api_diagnose_plant, name='api_diagnose_plant'),
    path('api/newsletter/subscribe/', views.api_newsletter_subscribe, name='api_newsletter_subscribe'),
    path('api/profile/update/', views.api_profile_update, name='api_profile_update'),
]
