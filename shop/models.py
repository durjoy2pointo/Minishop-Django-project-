from django.db import models
from django.contrib.auth.models import User

# =========================
#       PRODUCT TABLE
# =========================

GENDER_CHOICES = (
    ('men', 'Men'),
    ('women', 'Women'),
)

CATEGORY_CHOICES = (
    ('sport_shoes', 'Sport Shoes'),
    ('casual_shoes', 'Casual Shoes'),
    ('formal_shoes', 'Formal Shoes'),
    ('slider', 'Slider'),
    ('bag', 'Bag'),
    ('belt', 'Belt'),
    ('watch', 'Watch'),
    ('sunglasses', 'Sunglasses'),
)


class Product(models.Model):
    picture = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=200)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


#==================
# address table
#==================


class Address(models.Model):

    ADDRESS_TYPE_CHOICES = (
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPE_CHOICES
    )

    contact_number = models.CharField(max_length=15)
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    thana = models.CharField(max_length=100)
    corporation_or_union = models.CharField(max_length=150)
    area_or_village = models.CharField(max_length=200)

    additional_info = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.address_type}"
    


#========================
#       CART TABLE
#========================
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        price = self.product.discount_price or self.product.price
        return price * self.quantity

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"

#========================
#       ORDER TABLE
#========================

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Cash On Delivery'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('sslcommerz', 'SSLCommerz'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    address = models.ForeignKey(
        'Address',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"
    
