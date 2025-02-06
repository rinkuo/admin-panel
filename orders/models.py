from django.utils import timezone
from django.db import models
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def get_status_color(self):
        status_colors = {
            'pending': 'yellow',
            'processing': 'orange',
            'shipped': 'blue',
            'delivered': 'grey',
            'cancelled': 'red',
        }
        return status_colors.get(self.status, 'green')

    customer_name = models.CharField(max_length=100, verbose_name="Mijoz ismi")
    customer_phone = models.CharField(max_length=20, verbose_name="Telefon")
    customer_email = models.EmailField(max_length=100, verbose_name="Email", blank=True)
    customer_address = models.CharField(max_length=255, verbose_name="Manzil", blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Jami summa")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_id = models.CharField(max_length=100)
    order_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"#{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"

    def total_price(self):
        return self.quantity * self.price
