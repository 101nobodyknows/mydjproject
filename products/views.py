from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import new_product, Cart, CartProduct, Order, OrderProduct
from django.db.models import Q
import random

def product(request):
    product_list = list(new_product.objects.all())
    random.shuffle(product_list)
    
    #search feature
    query = request.GET.get('query', '')
    results = []
    if query:
        results = list(new_product.objects.filter(
            Q(product_name__icontains=query) | 
            Q(product_desc__icontains=query) | 
            Q(product_category__icontains=query)
        ))
        random.shuffle(results)
        context = {
            'product_list': results,
            'query': query
        }
    else:
        context = {
            'product_list':product_list
        }
    return render(request, 'products/products.html', context)

def product_details(request, product_id):
    product_detail = new_product.objects.get(id=product_id)
    return render(request, 'products/product_detail.html', {'product_detail':product_detail})


#cart feature
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(new_product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_product.quantity += 1
        cart_product.save()
    return redirect('product')

@login_required
def add_to_cart_det(request, product_id):
    product = get_object_or_404(new_product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_product.quantity += 1
        cart_product.save()
    return redirect(reverse('product_details', args=[product_id]))

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_products = CartProduct.objects.filter(cart=cart)
    item_total = [item.product.product_price * item.quantity for item in cart_products]
    for price in item_total:
        item_total_price = price
    for item in cart_products:
        item.total_price = item.product.product_price * item.quantity
        
    # Calculate the overall total price of the cart
    total_price = sum(item.total_price for item in cart_products)
    context = {
        'cart': cart,
        'total':total_price,
        'item_total_price': item_total_price
        }
    return render(request, 'products/cart.html', context)

@login_required
def update_cart_quantity(request, cart_product_id, action):
    cart_product = get_object_or_404(CartProduct, id=cart_product_id)
    if action == 'increase':
        cart_product.quantity += 1
    elif action == 'decrease' and cart_product.quantity > 1:
        cart_product.quantity -= 1
    cart_product.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, id=cart_product_id)
    cart_product.delete()
    return redirect('cart')

#checkout system
@login_required
def proceed_to_checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(user=request.user, total=0)
    for cart_product in cart.cartproduct_set.all():
        order_product = OrderProduct.objects.create(
            order=order,
            product=cart_product.product,
            quantity=cart_product.quantity
        )
        order.total += cart_product.product.product_price * cart_product.quantity
        order.save()
    cart.delete()
    return redirect('checkout', order_id=order.id)

@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'products/checkout.html', context)