from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from delivery.models import Package


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get('remember_me')
                if not remember_me:
                    request.session.set_expiry(0)
                
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard showing sent and received packages"""
    # Get packages sent by user
    sent_packages = Package.objects.filter(sender_user=request.user).order_by('-created_at')
    
    # Get packages received by user (match by email)
    received_packages = Package.objects.filter(receiver_user=request.user).order_by('-created_at')
    
    # Calculate statistics
    total_sent = sent_packages.count()
    total_received = received_packages.count()
    pending_sent = sent_packages.exclude(status='delivered').count()
    
    context = {
        'sent_packages': sent_packages,
        'received_packages': received_packages,
        'total_sent': total_sent,
        'total_received': total_received,
        'pending_sent': pending_sent,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """User profile view and edit"""
    # Ensure profile exists before accessing it
    from .models import UserProfile
    UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile, user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/profile.html', context)
