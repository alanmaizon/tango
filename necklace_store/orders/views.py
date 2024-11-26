
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Order, ChainType, ChainLength, Material
from .forms import CustomUserCreationForm, ProductForm

def create_order_and_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            order = Order.objects.create(customer=request.user)  # Assuming user is logged in
            product = product_form.save(commit=False)
            product.order = order
            product.calculate_final_price()
            product.generate_stock_code()
            product.save()
            return redirect('order_detail', pk=order.id)
    else:
        product_form = ProductForm()
    return render(request, 'orders/order_product_form.html', {'form': product_form})


def create_product(request):
    chain_types = ChainType.objects.all()
    chain_lengths = ChainLength.objects.all()
    materials = Material.objects.all()
    # Render the form with options
    return render(request, "orders/product_form.html", {
        "form": ProductForm,
        "chain_types": [{"id": ct.id, "name": ct.type_name, "price": ct.price} for ct in chain_types],
        "chain_lengths": [{"id": cl.id, "name": cl.length, "price": cl.price} for cl in chain_lengths],
        "materials": [{"id": m.id, "name": m.material_name, "price": m.price} for m in materials],
    })

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
    return render(request, 'orders/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Replace with your login URL
