from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """Extended user registration form with profile fields"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'your.email@example.com', 'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '+1234567890', 'class': 'form-control'})
    )
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Your address', 'rows': 3, 'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Update the auto-created profile
            user.profile.phone = self.cleaned_data['phone']
            user.profile.address = self.cleaned_data['address']
            user.profile.save()
        return user


class UserLoginForm(forms.Form):
    """User login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    remember_me = forms.BooleanField(required=False, initial=True)


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.email = self.cleaned_data['email']
            self.user.save()
        if commit:
            profile.save()
        return profile
