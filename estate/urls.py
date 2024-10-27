from django.urls import path
from . import views

app_name = 'estate'

urlpatterns = [
    path('properties/', views.PropertyListCreateView.as_view(), name='property-list-create'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
    path('tenants/', views.TenantListCreateView.as_view(), name='tenant-list-create'),
    path('tenants/<int:pk>/', views.TenantDetailView.as_view(), name='tenant-detail'),
    path('payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
]
