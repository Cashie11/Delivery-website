from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Package, Customer, TrackingEvent
from .forms import TrackingSearchForm, PickupRequestForm, ContactForm, CreatePackageForm, ClaimPackageForm, UpdateTrackingForm
from django.utils import timezone
from datetime import datetime, timedelta


def home(request):
    """Homepage with hero section and quick tracking"""
    form = TrackingSearchForm()
    
    # Get some statistics for the homepage
    total_packages = Package.objects.count()
    delivered_packages = Package.objects.filter(status='delivered').count()
    
    context = {
        'form': form,
        'total_packages': total_packages,
        'delivered_packages': delivered_packages,
    }
    return render(request, 'home.html', context)


def track_package(request, tracking_number=None):
    """Track package page with search and results"""
    package = None
    tracking_events = []
    
    if request.method == 'POST':
        form = TrackingSearchForm(request.POST)
        if form.is_valid():
            tracking_number = form.cleaned_data['tracking_number'].upper()
            return redirect('track_package_detail', tracking_number=tracking_number)
    else:
        form = TrackingSearchForm()
        
        if tracking_number:
            try:
                package = Package.objects.get(tracking_number=tracking_number.upper())
                tracking_events = package.tracking_events.all()
            except Package.DoesNotExist:
                messages.error(request, f'Package with tracking number {tracking_number} not found.')
    
    context = {
        'form': form,
        'package': package,
        'tracking_events': tracking_events,
    }
    return render(request, 'track.html', context)


def request_pickup(request):
    """Request pickup form page"""
    if request.method == 'POST':
        form = PickupRequestForm(request.POST)
        if form.is_valid():
            # Create sender customer
            sender = Customer.objects.create(
                name=form.cleaned_data['sender_name'],
                email=form.cleaned_data['sender_email'],
                phone=form.cleaned_data['sender_phone'],
                address=form.cleaned_data['sender_address']
            )
            
            # Create receiver customer
            receiver = Customer.objects.create(
                name=form.cleaned_data['receiver_name'],
                email=form.cleaned_data['receiver_email'],
                phone=form.cleaned_data['receiver_phone'],
                address=form.cleaned_data['receiver_address']
            )
            
            # Create package
            estimated_delivery = datetime.now().date() + timedelta(days=3)
            package = Package.objects.create(
                sender=sender,
                receiver=receiver,
                description=form.cleaned_data['description'],
                weight=form.cleaned_data['weight'],
                status='pending',
                current_location='Awaiting Pickup',
                estimated_delivery=estimated_delivery
            )
            
            # Create initial tracking event
            TrackingEvent.objects.create(
                package=package,
                status='pending',
                location='Pickup Requested',
                notes=f"Pickup requested for {form.cleaned_data.get('preferred_pickup_date', 'ASAP')}"
            )
            
            messages.success(
                request,
                f'Pickup request submitted successfully! Your tracking number is: {package.tracking_number}'
            )
            return redirect('track_package_detail', tracking_number=package.tracking_number)
    else:
        form = PickupRequestForm()
    
    context = {'form': form}
    return render(request, 'request_pickup.html', context)


@login_required
def create_package(request):
    """Create package view for authenticated users"""
    if request.method == 'POST':
        form = CreatePackageForm(request.POST, request.FILES)
        if form.is_valid():
            # Create sender customer from logged-in user
            sender = Customer.objects.create(
                name=request.user.get_full_name() or request.user.username,
                email=request.user.email,
                phone=request.user.profile.phone,
                address=request.user.profile.address
            )
            
            # Create receiver customer
            receiver = Customer.objects.create(
                name=form.cleaned_data['receiver_name'],
                email=form.cleaned_data['receiver_email'],
                phone=form.cleaned_data['receiver_phone'],
                address=form.cleaned_data['receiver_address']
            )
            
            # Calculate delivery time based on service tier
            tier_days = {
                'standard': 4,
                'express': 2,
                'same_day': 0
            }
            days = tier_days.get(form.cleaned_data['service_tier'], 4)
            estimated_delivery = datetime.now().date() + timedelta(days=days)
            
            # Create package
            package = Package.objects.create(
                sender=sender,
                receiver=receiver,
                sender_user=request.user,
                description=form.cleaned_data['description'],
                weight=form.cleaned_data['weight'],
                service_tier=form.cleaned_data['service_tier'],
                package_image=form.cleaned_data.get('package_image'),
                status='pending',
                current_location='Processing',
                estimated_delivery=estimated_delivery,
                payment_status='paid'  # Simulated payment
            )
            
            # Create initial tracking event
            TrackingEvent.objects.create(
                package=package,
                status='pending',
                location='Package Created',
                notes=f"Package created via user dashboard. Service: {package.get_service_tier_display()}"
            )
            
            messages.success(
                request,
                f'Package created successfully! Tracking number: {package.tracking_number}. Total: ${package.price}'
            )
            return redirect('package_success', tracking_number=package.tracking_number)
    else:
        form = CreatePackageForm()
    
    context = {'form': form}
    return render(request, 'delivery/create_package.html', context)


def claim_package(request):
    """View for receivers to verify and claim their package"""
    package = None
    if request.method == 'POST':
        form = ClaimPackageForm(request.POST)
        if form.is_valid():
            tracking_number = form.cleaned_data['tracking_number'].upper()
            verification_code = form.cleaned_data['verification_code']
            
            try:
                package = Package.objects.get(
                    tracking_number=tracking_number,
                    verification_code=verification_code
                )
                if package.is_claimed:
                    messages.warning(request, "This package has already been claimed.")
                    package = None
            except Package.DoesNotExist:
                messages.error(request, "Invalid tracking number or verification code.")
    else:
        form = ClaimPackageForm()
        
    context = {
        'form': form,
        'package': package,
    }
    return render(request, 'delivery/claim_package.html', context)


@login_required
def confirm_claim(request, tracking_number):
    """Action to mark package as received"""
    package = get_object_or_404(Package, tracking_number=tracking_number)
    
    if package.is_claimed:
        messages.warning(request, "Package already marked as received.")
        return redirect('dashboard')
        
    package.is_claimed = True
    package.claimed_at = timezone.now()
    package.status = 'delivered'
    package.current_location = 'Delivered to Receiver'
    package.save()
    
    # Add tracking event
    TrackingEvent.objects.create(
        package=package,
        status='delivered',
        location='Destination',
        notes=f"Package successfully claimed and received by the receiver."
    )
    
    messages.success(request, f"Package {tracking_number} has been marked as received! 🎉")
    return redirect('dashboard')


def services(request):
    """Services and pricing page"""
    return render(request, 'services.html')


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # In a real application, you would send an email here
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'contact.html', context)
@login_required
def update_package_status(request, tracking_number):
    """View for admins to update package status and location"""
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to update package status.")
        return redirect('dashboard')
        
    package = get_object_or_404(Package, tracking_number=tracking_number)
    
    if package.status == 'delivered':
        messages.warning(request, "This package has already been delivered.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UpdateTrackingForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            location = form.cleaned_data['current_location']
            notes = form.cleaned_data['notes']
            
            # Update package
            package.status = status
            package.current_location = location
            package.save()
            
            # Create tracking event
            TrackingEvent.objects.create(
                package=package,
                status=status,
                location=location,
                notes=notes or f"Status updated by sender."
            )
            
            messages.success(request, f"Tracking updated for {tracking_number}!")
            return redirect('dashboard')
    else:
        form = UpdateTrackingForm(initial={
            'status': package.status,
            'current_location': package.current_location
        })
        
    context = {
        'form': form,
        'package': package,
    }
    return render(request, 'delivery/update_status.html', context)


@login_required
def package_success(request, tracking_number):
    """Success page after package creation"""
    package = get_object_or_404(Package, tracking_number=tracking_number, sender_user=request.user)
    
    context = {
        'package': package,
    }
    return render(request, 'delivery/package_success.html', context)
