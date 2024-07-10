from django.urls import path
from .views import product, add_to_cart, add_to_cart_det, cart, update_cart_quantity, remove_from_cart, proceed_to_checkout, checkout, product_details

urlpatterns = [
    path('', product, name='product'),
    path('product_details/<int:product_id>', product_details, name='product_details'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('add-to-cart-d/<int:product_id>/', add_to_cart_det, name='add_to_cart_det'),
    path('cart/', cart, name='cart'),
    path('update-cart-quantity/<int:cart_product_id>/<str:action>/', update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:cart_product_id>/', remove_from_cart, name='remove_from_cart'),
    path('proceed-to-checkout/', proceed_to_checkout, name='proceed_to_checkout'),
    path('checkout/<int:order_id>/', checkout, name='checkout'),
]