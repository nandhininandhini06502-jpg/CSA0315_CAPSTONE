from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('user', 'User / Investigator'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    department = models.CharField(max_length=100, blank=True, default='Forensics & Investigation')
    badge_id = models.CharField(max_length=50, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_evidence_user(self):
        return self.role == 'user'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
