from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Product, Address, Cart, CartItem
from django.contrib.auth import login, logout
from .forms import AddressForm, SignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
 

from .models import Cart, CartItem
# Create your views here.
def index(request):
    product = Product.objects.all()
    return render(request, 'index.html', {'product': product})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_single.html', {'product': product})

def shop_view(request):
    products = Product.objects.all()

    gender = request.GET.get('gender')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if gender:
        products = products.filter(gender=gender)

    if category:
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'shop.html', {
        'product': products
    })

# ==========================
#      User Authentication 
# ==========================

def signup_view(request):
    next_url = request.POST.get('next') or request.GET.get('next') or 'index'

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            request.session['next_after_address'] = next_url

            return redirect('add_address')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form,
        'next': next_url
    })


def login_view(request):
    message = request.GET.get('message')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'signin.html',{
        'form': form,
        'next': request.GET.get('next'),
        'message': message
    })



def logout_view(request):
    logout(request)
    return redirect('index')

#=========================
#     addresss view
#=========================
@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            return redirect('index')
    else:
        form = AddressForm()

    return render(request, 'address.html', {'form': form})


#=========================
#      Cart and Checkout
#=========================



@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)

    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()

    return redirect('cart')

def cart_view(request):
    # এখানে cart logic লিখবে
    return render(request, 'cart.html')


#=========================
#   checkout view
#=========================
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product').all()
    addresses = Address.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    subtotal = sum(item.total_price for item in cart_items)
    discount = 0

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        payment_method = request.POST.get('payment_method')

        selected_address = get_object_or_404(
            Address,
            id=address_id,
            user=request.user
        )

        if selected_address.district.strip().lower() == 'dhaka':
            delivery_charge = 60
        else:
            delivery_charge = 120

        total = subtotal + delivery_charge - discount

        order = Order.objects.create(
            user=request.user,
            address=selected_address,
            payment_method=payment_method,
            total_price=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discount_price or item.product.price
            )

        cart_items.delete()

        return redirect('order_success', order_id=order.id)

    selected_address = addresses.first()
    delivery_charge = 0

    if selected_address:
        if selected_address.district.strip().lower() == 'dhaka':
            delivery_charge = 60
        else:
            delivery_charge = 120

    total = subtotal + delivery_charge - discount

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'addresses': addresses,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'discount': discount,
        'total': total,
    })




#==========================
#   About, blog and Contact view 
#==========================
def about_view(request):
    return render(request, 'about.html')
def blog_view(request):
    return render(request, 'blog.html')
def contact_view(request):
    return render(request, 'contact.html')



#=========================
#   Update and Remove Cart Item 
#=========================



@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.select_related('product').all()

    subtotal = sum(item.total_price for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
    })


@login_required
@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()

    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')


@login_required
@require_POST
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect('cart')



#==========================
#  Order 
#=========================
@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(request, 'order_success.html', {
        'order': order
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    ).select_related(
        'address'
    ).prefetch_related(
        'items__product'
    ).order_by('-created_at')

    return render(request, 'order_history.html', {
        'orders': orders
    })