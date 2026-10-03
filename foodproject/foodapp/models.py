from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid


class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='restaurants/',
        blank=True,
        null=True
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Food(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        related_name='foods',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(blank=True)

    # Existing food records without image should not crash
    image = models.ImageField(
        upload_to='food/',
        blank=True,
        null=True
    )

    is_available = models.BooleanField(default=True)

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.city}"


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'food'],
                name='unique_user_food_cart'
            )
        ]

    def total_price(self):
        return self.food.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'food'],
                name='unique_user_food_wishlist'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"


class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True
    )

    order_number = models.CharField(
        max_length=40,
        unique=True,
        null=True,
        blank=True
    )

    # Old fields retained so existing project data doesn't break
    food_name = models.CharField(
        max_length=100,
        blank=True
    )

    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField(default=0)

    image = models.ImageField(
        upload_to='orders/',
        blank=True,
        null=True
    )

    address = models.TextField(blank=True)

    special_instruction = models.TextField(
        blank=True,
        null=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='COD'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    rating = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = (
                "FR"
                + timezone.now().strftime("%Y%m%d")
                + "-"
                + uuid.uuid4().hex[:8].upper()
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number or "Order"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.order.order_number} - {self.food}"


class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.IntegerField(default=5)
    comment = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"


class Contact(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class comment(models.Model):

    name = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name