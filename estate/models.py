from django.db import models
from authentication.models import CustomUser

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('land', 'Land'),
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('company', 'Company'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Tenant(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant}"