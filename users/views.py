from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.contrib import messages

from .forms import CustomUserCreationForm, ShoeForm, ShoeImageForm
from ecom.models import Shoes,Order, OrderItem, ShoeImage
from .models import CustomUser


def signup_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")  
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})



def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            

            if user:
                login(request, user)
                
                if user.is_staff:
                    return redirect(admin_page)
                return redirect('/')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
                
                
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form' : form})


def logout_page(request):
    logout(request)
    return redirect(login_page)

@staff_member_required
def admin_page(request):
    total_users = CustomUser.objects.count()
    total_products = Shoes.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(paid = 'True').aggregate(
        total = Sum('amount')
    )['total'] or 0

    context = {
        'total_products' : total_products,
        'total_orders' : total_orders,
        'total_users' : total_users,
        'total_revenue' : total_revenue / 100
    }
    return render(request, 'users/adminPage.html', context)

@staff_member_required
def admin_users(request):

    total_users = CustomUser.objects.all().order_by('-id')

    context = {
        'total_users' : total_users,
    }

    return render(request, 'users/adminUsers.html', context)

@staff_member_required
def admin_products(request):

    total_products = Shoes.objects.all().order_by('-id')

    context = {
        'total_products' : total_products
    }

    return render(request, 'users/adminProducts.html', context)


@staff_member_required
def admin_orders(request):

    total_orders = Order.objects.all().order_by('-id')

    for order in total_orders:
        order.amount = order.amount / 100

    context = {
        'total_orders' : total_orders
    }

    return render(request, 'users/adminOrders.html', context)

@staff_member_required
def admin_add_product(request):

    if request.method == 'POST':
        form = ShoeForm(request.POST, request.FILES)

        if form.is_valid():
            shoe = form.save()

            images = request.FILES.getlist('gallery_images')
            for image in images:
                ShoeImage.objects.create(shoe = shoe, image = image)
            
            return redirect('admin_products')
    else:
        form = ShoeForm()

    return render(request, 'users/addProduct.html',{'form' : form})


@staff_member_required
def admin_edit_product(request, product_id):

    product = get_object_or_404(Shoes, id = product_id)
    if request.method == 'POST':
        form = ShoeForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            shoe = form.save()

            images = request.FILES.getlist('gallery_images')
            for image in images:
                ShoeImage.objects.create(shoe = shoe, image = image)

            return redirect('admin_products')

    else:
        form = ShoeForm(instance=product)
    return render(request, 'users/editProduct.html',{'form' : form})

@staff_member_required
def admin_delete_product(request, product_id):

    product = get_object_or_404(Shoes, id = product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('admin_products')

    return render(request, 'users/deleteProduct.html',{'product' : product})

@staff_member_required
def admin_deactivate_user(request, user_id):

    user = get_object_or_404(CustomUser,id = user_id)
    if request.method == 'POST':
        user.is_active = False
        user.save()

        return redirect(admin_users)

    return render(request, 'users/deactivateUser.html',{'user' : user, 'action' : 'deactivate'})

@staff_member_required
def admin_activate_user(request, user_id):
    
    user = get_object_or_404(CustomUser, id = user_id)
    if request.method == 'POST':
        user.is_active = True
        user.save()

        return redirect(admin_users)
    
    
    return render(request, 'users/deactivateUser.html', {'user' : user, 'action' : 'activate'})