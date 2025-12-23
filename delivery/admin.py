from django.contrib import admin
from .models import Customer, Package, TrackingEvent


class TrackingEventInline(admin.TabularInline):
    """Inline admin for tracking events"""
    model = TrackingEvent
    extra = 1
    fields = ['status', 'location', 'notes', 'timestamp']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin configuration for Customer model"""
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['created_at']
    readonly_fields = ['created_at']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    """Admin configuration for Package model"""
    list_display = ['tracking_number', 'sender', 'receiver', 'service_tier', 'price', 'status', 'payment_status', 'created_at']
    search_fields = ['tracking_number', 'sender__name', 'receiver__name', 'sender_user__username']
    list_filter = ['status', 'service_tier', 'payment_status', 'created_at']
    readonly_fields = ['tracking_number', 'price', 'created_at', 'updated_at']
    inlines = [TrackingEventInline]
    fieldsets = (
        ('Package Information', {
            'fields': ('tracking_number', 'description', 'weight', 'service_tier', 'price', 'payment_status')
        }),
        ('Sender & Receiver', {
            'fields': ('sender', 'sender_user', 'receiver', 'receiver_user')
        }),
        ('Status & Location', {
            'fields': ('status', 'current_location', 'estimated_delivery')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrackingEvent)
class TrackingEventAdmin(admin.ModelAdmin):
    """Admin configuration for TrackingEvent model"""
    list_display = ['package', 'status', 'location', 'timestamp']
    search_fields = ['package__tracking_number', 'location']
    list_filter = ['status', 'timestamp']
    readonly_fields = ['timestamp']


# Customize admin site header and title
admin.site.site_header = "SwiftTrack Admin"
admin.site.site_title = "SwiftTrack Admin Portal"
admin.site.index_title = "Welcome to SwiftTrack Administration"
