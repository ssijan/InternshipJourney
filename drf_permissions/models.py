from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.conf import settings

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin',
        AGENT = 'AGENT', 'Agent'
        CUSTOMER = 'CUSTOMER', 'Customer'
    
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    bio = models.TextField(blank=True, null= True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        DISPUTED = 'DISPUTED', 'Disputed'
        REFUNDED = 'REFUNDED', 'Refunded'

    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transction'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant = models.CharField(max_length=250)
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tx {self.id} - {self.user.username} - ${self.amount}"
    


class SecureDocument(models.Model):
    title = models.CharField(max_length=255)
    confidential_content = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    class Meta:
            permissions = (
                ('edit_securedocument', 'Can edit specific secure document'),
            )

    def __str__(self):
        return self.title