import os
import json
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Package, Customer, TrackingEvent
from decimal import Decimal


def require_api_key(view_func):
    """Decorator to validate API-KEY header against SERVER-KEY env variable"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        api_key = request.headers.get('API-KEY')
        server_key = os.getenv('SERVER-KEY')
        
        if not server_key:
            return JsonResponse({
                'success': False,
                'error': 'Server configuration error: SERVER-KEY not configured'
            }, status=500)
        
        if not api_key:
            return JsonResponse({
                'success': False,
                'error': 'Authentication failed: API-KEY header is required'
            }, status=401)
        
        if api_key != server_key:
            return JsonResponse({
                'success': False,
                'error': 'Authentication failed: Invalid API-KEY'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


@csrf_exempt
@require_http_methods(["POST"])
@require_api_key
def create_package_api(request):
    """
    API endpoint to create a package
    
    Expected JSON payload:
    {
        "sender": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "address": "123 Main St, City, Country"
        },
        "receiver": {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "+0987654321",
            "address": "456 Oak Ave, City, Country"
        },
        "description": "Electronics",
        "weight": 2.5,
        "service_tier": "express",  // optional: standard, express, same_day
        "current_location": "Warehouse A"  // optional
    }
    """
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['sender', 'receiver', 'description', 'weight']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=400)
        
        # Validate sender and receiver have required fields
        customer_fields = ['name', 'email', 'phone', 'address']
        for party in ['sender', 'receiver']:
            missing = [f for f in customer_fields if f not in data[party]]
            if missing:
                return JsonResponse({
                    'success': False,
                    'error': f'Missing {party} fields: {", ".join(missing)}'
                }, status=400)
        
        # Create or get sender
        sender, _ = Customer.objects.get_or_create(
            email=data['sender']['email'],
            defaults={
                'name': data['sender']['name'],
                'phone': data['sender']['phone'],
                'address': data['sender']['address']
            }
        )
        
        # Create or get receiver
        receiver, _ = Customer.objects.get_or_create(
            email=data['receiver']['email'],
            defaults={
                'name': data['receiver']['name'],
                'phone': data['receiver']['phone'],
                'address': data['receiver']['address']
            }
        )
        
        # Create package
        package = Package.objects.create(
            sender=sender,
            receiver=receiver,
            description=data['description'],
            weight=Decimal(str(data['weight'])),
            service_tier=data.get('service_tier', 'standard'),
            current_location=data.get('current_location', 'Processing Center')
        )
        
        # Create initial tracking event
        TrackingEvent.objects.create(
            package=package,
            status='pending',
            location=package.current_location,
            notes='Package created via API'
        )
        
        # Prepare response
        response_data = {
            'success': True,
            'message': 'Package created successfully',
            'data': {
                'tracking_number': package.tracking_number,
                'verification_code': package.verification_code,
                'status': package.status,
                'service_tier': package.service_tier,
                'price': str(package.price),
                'payment_status': package.payment_status,
                'current_location': package.current_location,
                'estimated_delivery': package.estimated_delivery.isoformat() if package.estimated_delivery else None,
                'sender': {
                    'name': sender.name,
                    'email': sender.email,
                    'phone': sender.phone,
                    'address': sender.address
                },
                'receiver': {
                    'name': receiver.name,
                    'email': receiver.email,
                    'phone': receiver.phone,
                    'address': receiver.address
                },
                'description': package.description,
                'weight': str(package.weight),
                'created_at': package.created_at.isoformat()
            }
        }
        
        return JsonResponse(response_data, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON payload'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@require_api_key
def track_package_api(request, tracking_number):
    """
    API endpoint to track a package
    
    URL: /api/track/<tracking_number>/
    """
    try:
        package = Package.objects.select_related('sender', 'receiver').get(
            tracking_number=tracking_number
        )
        
        # Get tracking events
        tracking_events = package.tracking_events.all()
        
        response_data = {
            'success': True,
            'data': {
                'tracking_number': package.tracking_number,
                'status': package.status,
                'status_display': package.get_status_display(),
                'service_tier': package.service_tier,
                'service_tier_display': package.get_service_tier_display(),
                'price': str(package.price),
                'payment_status': package.payment_status,
                'current_location': package.current_location,
                'estimated_delivery': package.estimated_delivery.isoformat() if package.estimated_delivery else None,
                'is_claimed': package.is_claimed,
                'claimed_at': package.claimed_at.isoformat() if package.claimed_at else None,
                'sender': {
                    'name': package.sender.name,
                    'email': package.sender.email,
                    'phone': package.sender.phone,
                    'address': package.sender.address
                },
                'receiver': {
                    'name': package.receiver.name,
                    'email': package.receiver.email,
                    'phone': package.receiver.phone,
                    'address': package.receiver.address
                },
                'description': package.description,
                'weight': str(package.weight),
                'created_at': package.created_at.isoformat(),
                'updated_at': package.updated_at.isoformat(),
                'tracking_history': [
                    {
                        'status': event.status,
                        'status_display': event.get_status_display(),
                        'location': event.location,
                        'notes': event.notes,
                        'timestamp': event.timestamp.isoformat()
                    }
                    for event in tracking_events
                ]
            }
        }
        
        return JsonResponse(response_data, status=200)
    
    except Package.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'Package with tracking number {tracking_number} not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)
