from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Order, ChainType, ChainLength, Material, FontStyle
from .forms import CustomUserCreationForm, ProductForm

def create_product(request):
    if request.method == "POST":
        print(request.POST)  # Debug the submitted POST data
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.calculate_final_price()
            product.generate_stock_code()
            product.save()
            return redirect('home')
        else:
            print(form.errors)  # Debug form errors
    else:
        form = ProductForm()
    chain_types = ChainType.objects.all()
    chain_lengths = ChainLength.objects.all()
    materials = Material.objects.all()
    font_styles = FontStyle.objects.all()
    return render(request, "orders/product_form.html", {
        "form": form,
        "chain_types": chain_types,
        "chain_lengths": chain_lengths,
        "materials": materials,
        "font_styles": font_styles,
    })

@login_required
def create_order_and_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            order = Order.objects.create(customer=request.user)
            product = product_form.save(commit=False)
            product.order = order
            product.calculate_final_price()
            product.generate_stock_code()
            product.save()
            return redirect('order_detail', pk=order.id)
        else:
            print(product_form.errors)  # Debugging form errors
    else:
        product_form = ProductForm()
    return render(request, 'orders/order_product_form.html', {'form': product_form})


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.calculate_final_price()
            product.generate_stock_code()
            product.save()
            return redirect('home')  # Replace with appropriate success URL
        else:
            print(form.errors)  # Debug form errors
    else:
        form = ProductForm()
    return render(request, "orders/product_form.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace with your homepage URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'orders/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'orders/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Replace with your login URL
