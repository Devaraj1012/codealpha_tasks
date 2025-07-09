from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL for homepage

    # Product detail page, using pk as URL parameter
    path('product/<int:pk>/', views.product_detail, name='product-detail'),

    # User authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout URL
    path('checkout/', views.checkout_view, name='checkout'),
]
