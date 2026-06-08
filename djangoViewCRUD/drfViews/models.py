from django.db import models
from django.contrib.auth.models import User
 
class BankAccount(models.Model):
    ACCOUNT_TYPES = [("savings", "Savings"), ("checking", "Checking")]
    STATUS_CHOICES = [("active", "Active"), ("frozen", "Frozen"), ("closed", "Closed")]
 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="drf_accounts")
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default="savings")
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["-created_at"]
 
    def __str__(self):
        return f"{self.account_number} ({self.owner.username})"
    

