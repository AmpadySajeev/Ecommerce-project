from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup_page, name = 'signup'),
    path('login', login_page, name = 'login'),
    path('logout', logout_page, name = 'logout'),
    path('admin-page', admin_page, name = 'admin_page'),
    path('admin-products', admin_products, name = 'admin_products'),
    path('total-users', admin_users, name = 'adminUsers'),
    path('total-orders', admin_orders, name = 'adminOrders'),
    path('admin_add_product', admin_add_product, name = 'add_product'),
    path('admin_edit_product/<int:product_id>', admin_edit_product, name = 'edit_product'),
    path('admin_delete_product/<int:product_id>', admin_delete_product, name = 'delete_product'),
    path('admin_restrict_action<int:user_id>', admin_deactivate_user, name = 'deactivate_user'),
    path('admin_activate_user/<int:user_id>', admin_activate_user, name = 'activate_user'),
]