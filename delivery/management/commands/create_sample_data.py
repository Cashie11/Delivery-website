from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from delivery.models import Customer, Package, TrackingEvent
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **kwargs):
        # Set admin password
        try:
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin password set to: admin123'))
        except User.DoesNotExist:
            pass

        # Create sample customers
        sender1 = Customer.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            phone="+1-555-0101",
            address="123 Main St, New York, NY 10001"
        )
        
        receiver1 = Customer.objects.create(
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="+1-555-0202",
            address="456 Oak Ave, Los Angeles, CA 90001"
        )
        
        sender2 = Customer.objects.create(
            name="Bob Johnson",
            email="bob.johnson@example.com",
            phone="+1-555-0303",
            address="789 Pine Rd, Chicago, IL 60601"
        )
        
        receiver2 = Customer.objects.create(
            name="Alice Williams",
            email="alice.williams@example.com",
            phone="+1-555-0404",
            address="321 Elm St, Houston, TX 77001"
        )

        # Create sample packages
        package1 = Package.objects.create(
            sender=sender1,
            receiver=receiver1,
            description="Electronics - Laptop",
            weight=2.5,
            status='delivered',
            current_location='Los Angeles Distribution Center',
            estimated_delivery=datetime.now().date() - timedelta(days=1)
        )
        
        # Add tracking events for package1
        TrackingEvent.objects.create(
            package=package1,
            status='pending',
            location='New York Pickup Center',
            notes='Package received and processed',
            timestamp=datetime.now() - timedelta(days=4, hours=10)
        )
        TrackingEvent.objects.create(
            package=package1,
            status='picked_up',
            location='New York Pickup Center',
            notes='Package picked up by courier',
            timestamp=datetime.now() - timedelta(days=4, hours=8)
        )
        TrackingEvent.objects.create(
            package=package1,
            status='in_transit',
            location='Memphis Distribution Hub',
            notes='In transit to destination',
            timestamp=datetime.now() - timedelta(days=3, hours=14)
        )
        TrackingEvent.objects.create(
            package=package1,
            status='in_transit',
            location='Los Angeles Distribution Center',
            notes='Arrived at destination facility',
            timestamp=datetime.now() - timedelta(days=1, hours=6)
        )
        TrackingEvent.objects.create(
            package=package1,
            status='out_for_delivery',
            location='Los Angeles Local Depot',
            notes='Out for delivery',
            timestamp=datetime.now() - timedelta(hours=8)
        )
        TrackingEvent.objects.create(
            package=package1,
            status='delivered',
            location='456 Oak Ave, Los Angeles, CA 90001',
            notes='Delivered successfully - Signed by recipient',
            timestamp=datetime.now() - timedelta(hours=2)
        )

        package2 = Package.objects.create(
            sender=sender2,
            receiver=receiver2,
            description="Books and Documents",
            weight=1.2,
            status='in_transit',
            current_location='Dallas Distribution Hub',
            estimated_delivery=datetime.now().date() + timedelta(days=2)
        )
        
        TrackingEvent.objects.create(
            package=package2,
            status='pending',
            location='Chicago Pickup Center',
            notes='Package received',
            timestamp=datetime.now() - timedelta(days=2, hours=5)
        )
        TrackingEvent.objects.create(
            package=package2,
            status='picked_up',
            location='Chicago Pickup Center',
            notes='Picked up and in transit',
            timestamp=datetime.now() - timedelta(days=2, hours=3)
        )
        TrackingEvent.objects.create(
            package=package2,
            status='in_transit',
            location='Dallas Distribution Hub',
            notes='Package in transit',
            timestamp=datetime.now() - timedelta(days=1, hours=10)
        )

        package3 = Package.objects.create(
            sender=sender1,
            receiver=receiver2,
            description="Clothing and Accessories",
            weight=0.8,
            status='pending',
            current_location='Awaiting Pickup',
            estimated_delivery=datetime.now().date() + timedelta(days=5)
        )
        
        TrackingEvent.objects.create(
            package=package3,
            status='pending',
            location='Pickup Requested',
            notes='Pickup scheduled for tomorrow',
            timestamp=datetime.now() - timedelta(hours=3)
        )

        self.stdout.write(self.style.SUCCESS(f'Created sample data:'))
        self.stdout.write(f'  - Package 1 (Delivered): {package1.tracking_number}')
        self.stdout.write(f'  - Package 2 (In Transit): {package2.tracking_number}')
        self.stdout.write(f'  - Package 3 (Pending): {package3.tracking_number}')
