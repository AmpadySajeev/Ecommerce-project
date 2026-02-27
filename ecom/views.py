from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import razorpay
from django.conf import settings

from .models import Shoes,Category,ShoeImage, Cart, Order, OrderItem

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def cartpage(request):
    return render(request, 'cart.html')

def productsPage(request):
    shoes = Shoes.objects.all()
    return render(request, 'productListing.html', {'shoes' : shoes})

def filteredProducts(request, category_slug):

    category = get_object_or_404(Category, slug = category_slug)
    shoes = Shoes.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'filteredProducts.html',{'category' : category, 'shoes' : shoes, 'categories' : categories})

def detailPage(request, shoe_id):
    shoe = get_object_or_404(Shoes, id = shoe_id)
    shoe_image = ShoeImage.objects.filter(shoe=shoe)
    return render(request, 'productDetail.html',{'shoe' : shoe, 'shoe_image' : shoe_image})

def order_history(request):

    total_orders = Order.objects.filter(user = request.user).order_by('-id')

    context = {
        'items' : total_orders,
    }

    return render(request, 'orderHistory.html', context)

#CART

@login_required
def add_to_cart(request, shoe_id):
    shoe = get_object_or_404(Shoes, id = shoe_id)
    print('DEBUG adding cart for user', request.user)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=shoe)

    if not created:
        cart_item.quantity+=1
        cart_item.save()
    
    return redirect('view_cart')

@login_required
def view_cart(request):

    print('DEBUG view cart for user', request.user)
    cart_items = Cart.objects.filter(user=request.user)
    print('Debug cart items: ', cart_items)
    total_price = sum(item.get_total_price() for item in cart_items)

    
    return render(request, 'cart.html',{'cart_items' : cart_items, 'total_price' : total_price})

@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id = cart_id, user = request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
            
    return redirect(view_cart)

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id = cart_id, user=request.user)
    cart_item.delete()
    return redirect(view_cart)

def search_products(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        results = Shoes.objects.filter(name__contains=searched)
        return render(request, 'searchpage.html',{'searched' : searched, 'results' : results})
    else:
        return render(request, 'searchpage.html')


def checkout(request):

    cart_items = Cart.objects.filter( user = request.user)

    if not cart_items.exists():
        return redirect(view_cart)
    
    total_amount = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if not full_name or not phone or not address:
            messages.error(request, 'All feilds are required')
            return redirect(checkout)
        
        request.session['checkout_data'] = {
            'full_name' : full_name,
            'phone' : phone,
            'address' : address
        }

        return redirect(payment)
    
    context = {
        'cart_items' : cart_items,
        'total_amount' : total_amount
    }

    return render(request, 'checkout.html', context)

@login_required
def payment(request):

    cart_items = Cart.objects.filter( user = request.user)

    if not cart_items.exists():
        return redirect(view_cart)
    
    total_amount = sum(item.get_total_price() for item in cart_items)
    amount_paise = int(total_amount * 100)

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    razorpay_order = client.order.create({
        'amount' : amount_paise,
        'currency' : 'INR',
        'payment_capture' : 1
    })

    request.session['razorpay_order_id'] = razorpay_order['id']

    context = {
        'razorpay_order_id' : razorpay_order['id'],
        'razorpay_key' : settings.RAZORPAY_KEY_ID,
        'amount' : total_amount,
        'amount_paise' : amount_paise,
        'user' : request.user
    }
    
    return render(request, 'payment.html', context)

def payment_failed(request):

    return render(request, 'paymentFail.html')

@csrf_exempt
def payment_success(request):

    payment_id = request.GET.get('payment_id')
    signature = request.GET.get('signature')

    razorpay_order_id = request.session.get('razorpay_order_id')
    checkout_data = request.session.get('checkout_data')

    if not payment_id or not signature or not razorpay_order_id or not checkout_data:
        return render(request, 'paymentFail.html')

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    params_dict = {
        'razorpay_order_id' : razorpay_order_id,
        'razorpay_payment_id' : payment_id,
        'razorpay_signature' : signature
    }

    try:

        client.utility.verify_payment_signature(params_dict)

        cart_items = Cart.objects.filter(user = request.user)
        total_amount = sum(item.get_total_price() for item in cart_items)
        

        order = Order.objects.create(
            user = request.user,
            razorpay_order_id = razorpay_order_id,
            razorpay_payment_id = payment_id,
            razorpay_signature = signature,
            amount = total_amount,
            paid = True,
            full_name = checkout_data['full_name'],
            phone = checkout_data['phone'],
            address = checkout_data['address']
        )

        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price
            )

        cart_items.delete()

        del request.session['checkout_data']
        del request.session['razorpay_order_id']

        return render(request, 'paymentSuccess.html')
    
    except Exception as e:
        print(f"Payment verification failed: {e}")
        return render(request, 'paymentFail.html')

        


