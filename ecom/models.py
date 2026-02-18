from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Shoes(models.Model):
    name = models.CharField(max_length=200, null=True)
    brand = models.CharField(max_length=50, default='Adidas', null=True)
    image = models.ImageField(upload_to='products', null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(decimal_places=2,max_digits=8, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    is_featured = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.name}"

class ShoeImage(models.Model):
    shoe = models.ForeignKey(Shoes, on_delete=models.CASCADE, related_name='shoe_image')
    image = models.ImageField(upload_to='shoe_gallery')

    def __str__(self):
        return f"{self.shoe}"
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product} ({self.user.name})"
    
    def get_total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField(null=True)
    paid = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    full_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
