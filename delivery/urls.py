from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.home, name='home'),
    path('track/', views.track_package, name='track_package'),
    path('track/<str:tracking_number>/', views.track_package, name='track_package_detail'),
    path('request-pickup/', views.request_pickup, name='request_pickup'),
    path('create-package/', views.create_package, name='create_package'),
    path('package-success/<str:tracking_number>/', views.package_success, name='package_success'),
    path('claim-package/', views.claim_package, name='claim_package'),
    path('confirm-claim/<str:tracking_number>/', views.confirm_claim, name='confirm_claim'),
    path('update-status/<str:tracking_number>/', views.update_package_status, name='update_package_status'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    
    # API endpoints
    path('api/packages/create/', api_views.create_package_api, name='api_create_package'),
    path('api/packages/track/<str:tracking_number>', api_views.track_package_api, name='api_track_package'),
]
