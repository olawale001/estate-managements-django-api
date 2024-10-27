from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser 
from django.core.mail import send_mail
from authentication.views import IsAdmin
from .models import Property, Tenant, Payment
from .serializers import PropertySerializer, TenantSerializer, PaymentSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user



class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'property_type', 'is_available']
    pagination_class = StandardResultsSetPagination

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]



class TenantListCreateView(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']
    pagination_class = StandardResultsSetPagination

class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    parser_classes = [MultiPartParser, FormParser]


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    parser_classes = [MultiPartParser, FormParser]


    def perform_create(self, serializer):
        
        tenant = serializer.validated_data['tenant']
        amount = serializer.validated_data['amount']
        send_mail(
            'Payment Received',
            f'Thank you, {tenant.first_name}, for your payment of {amount}.',
            'olacodeire@gmail.com',
            [tenant.email],
            fail_silently=False,
        )
        serializer.save()

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer    
    parser_classes = [MultiPartParser, FormParser]
    