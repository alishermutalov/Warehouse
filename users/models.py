import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

MANAGER, ADMIN, ORDINARY_USER = "manager", "admin", "ordinary_user"

class User(AbstractUser):
    ROLE = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=30, choices=ROLE, default=ORDINARY_USER)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
        
    