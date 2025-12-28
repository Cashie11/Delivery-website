from django import forms
from .models import Customer, Package


class TrackingSearchForm(forms.Form):
    """Form for searching packages by tracking number"""
    tracking_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter tracking number',
            'class': 'tracking-input'
        })
    )


class PickupRequestForm(forms.Form):
    """Form for requesting package pickup"""
    # Sender Information
    sender_name = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'form-control'})
    )
    sender_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'your.email@example.com', 'class': 'form-control'})
    )
    sender_phone = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'placeholder': '+1234567890', 'class': 'form-control'})
    )
    sender_address = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Pickup address', 'rows': 3, 'class': 'form-control'})
    )
    
    # Receiver Information
    receiver_name = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'placeholder': 'Recipient name', 'class': 'form-control'})
    )
    receiver_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'recipient@example.com', 'class': 'form-control'})
    )
    receiver_phone = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'placeholder': '+1234567890', 'class': 'form-control'})
    )
    receiver_address = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Delivery address', 'rows': 3, 'class': 'form-control'})
    )
    
    # Package Information
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Package description', 'rows': 3, 'class': 'form-control'})
    )
    weight = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'Weight in kg', 'step': '0.01', 'class': 'form-control'})
    )
    preferred_pickup_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )


class ContactForm(forms.Form):
    """Form for contact inquiries"""
    name = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'your.email@example.com', 'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your message', 'rows': 5, 'class': 'form-control'})
    )


class CreatePackageForm(forms.Form):
    """Form for authenticated users to create packages"""
    # Receiver Information
    receiver_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Recipient name', 'class': 'form-control'})
    )
    receiver_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'recipient@example.com', 'class': 'form-control'})
    )
    receiver_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '+1234567890', 'class': 'form-control'})
    )
    receiver_address = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Delivery address', 'rows': 3, 'class': 'form-control'})
    )
    
    # Package Information
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Package description', 'rows': 3, 'class': 'form-control'})
    )
    weight = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'Weight in kg', 'step': '0.01', 'class': 'form-control', 'id': 'weight-input'})
    )
    service_tier = forms.ChoiceField(
        choices=Package.SERVICE_TIER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'tier-radio'}),
        initial='standard'
    )
    package_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )


class ClaimPackageForm(forms.Form):
    """Form for claiming a package"""
    tracking_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 12-digit Tracking Number', 'class': 'form-control'})
    )
    verification_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit Verification Code', 'class': 'form-control'})
    )

class UpdateTrackingForm(forms.Form):
    """Form for senders to update package status and location"""
    status = forms.ChoiceField(
        choices=Package.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    current_location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Current city/facility', 'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Additional notes (optional)', 'rows': 2, 'class': 'form-control'})
    )
