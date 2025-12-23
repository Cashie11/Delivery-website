from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import random
import string


class Customer(models.Model):
    """Model for storing customer (sender/receiver) information"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Package(models.Model):
    """Model for package tracking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ]
    
    SERVICE_TIER_CHOICES = [
        ('standard', 'Standard (3-5 days)'),
        ('express', 'Express (1-2 days)'),
        ('same_day', 'Same-Day'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    tracking_number = models.CharField(max_length=12, unique=True, editable=False)
    
    # User relationships (nullable for backward compatibility)
    sender_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='sent_packages'
    )
    receiver_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='received_packages'
    )
    
    # Customer relationships (for non-registered users)
    sender = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='sent_packages'
    )
    receiver = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='received_packages'
    )
    
    # Package details
    description = models.TextField()
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in kg")
    
    # Service and pricing
    service_tier = models.CharField(
        max_length=20, 
        choices=SERVICE_TIER_CHOICES, 
        default='standard'
    )
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0.00,
        help_text="Total price in USD"
    )
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending'
    )
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    current_location = models.CharField(max_length=200, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    
    # Verification and Claiming
    package_image = models.ImageField(upload_to='packages/', null=True, blank=True)
    verification_code = models.CharField(max_length=6, editable=False)
    is_claimed = models.BooleanField(default=False)
    claimed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        if not self.verification_code:
            self.verification_code = self.generate_verification_code()
        # Auto-calculate price if not set
        if self.price == 0:
            self.price = self.calculate_price()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_tracking_number():
        """Generate a unique 12-character alphanumeric tracking number"""
        while True:
            tracking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            if not Package.objects.filter(tracking_number=tracking_number).exists():
                return tracking_number
    
    @staticmethod
    def generate_verification_code():
        """Generate a random 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))
    
    def calculate_price(self):
        """Calculate price based on service tier and weight"""
        # Base prices
        base_prices = {
            'standard': Decimal('9.99'),
            'express': Decimal('19.99'),
            'same_day': Decimal('39.99'),
        }
        
        # Per kg rates
        per_kg_rates = {
            'standard': Decimal('2.00'),
            'express': Decimal('3.00'),
            'same_day': Decimal('4.00'),
        }
        
        base = base_prices.get(self.service_tier, Decimal('9.99'))
        rate = per_kg_rates.get(self.service_tier, Decimal('2.00'))
        
        total = base + (Decimal(str(self.weight)) * rate)
        return round(total, 2)

    def get_status_color(self):
        """Return color code for status badge"""
        colors = {
            'pending': '#6B7280',
            'picked_up': '#3B82F6',
            'in_transit': '#8B5CF6',
            'out_for_delivery': '#F59E0B',
            'delivered': '#10B981',
        }
        return colors.get(self.status, '#6B7280')

    class Meta:
        ordering = ['-created_at']


class TrackingEvent(models.Model):
    """Model for tracking package history"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='tracking_events')
    status = models.CharField(max_length=20, choices=Package.STATUS_CHOICES)
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.package.tracking_number} - {self.get_status_display()} at {self.location}"

    class Meta:
        ordering = ['-timestamp']
