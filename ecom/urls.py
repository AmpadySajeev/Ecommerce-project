from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage, name = 'home'),
    path('products', productsPage, name = 'products'),
    path('filtered-category/<slug:category_slug>', filteredProducts, name = 'filteredProducts'),
    path('product-details/<int:shoe_id>', detailPage, name = 'detailPage'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:shoe_id>', add_to_cart, name = 'add_to_cart'),
    path('cart/remove/<int:cart_id>', remove_from_cart, name = 'remove_from_cart'),
    path('cart/update/<int:cart_id>', update_cart, name='update_cart'),
    path('search/', search_products, name='search'),
    path('checkout/', checkout, name='checkout'),
    path('payment-success/', payment_success, name='payment-success'),
    path('order-history', order_history, name = 'order_history'),
    path('payment', payment, name = 'payment')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)