from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required

# Home Page showing product list
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# Product Detail Page
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# User Registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home after registration
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

# User Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after login
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

# User Logout
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Redirect to home after logout

# Cart View
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        total += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

# Add product to Cart
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

# Remove product from Cart
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
    return redirect('cart')

# Checkout View (Login Required)
@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home')

    products = Product.objects.filter(id__in=cart.keys())
    total = sum(product.price * cart[str(product.id)] for product in products)

    order = Order.objects.create(user=request.user, total_price=total)
    for product in products:
        quantity = cart[str(product.id)]
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

    request.session['cart'] = {}  # Clear cart after order

    return render(request, 'store/checkout.html', {'order': order})
