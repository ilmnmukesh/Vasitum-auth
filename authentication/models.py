from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError("Users should have email")

        user= self.model(email=self.normalize_email(email), password=password)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password):
        if password  is None:
            raise TypeError("Password should not None")
        
        user=self.create_user(email, password)
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    PROVIDER        = (
        ("default", "default"),
        ("Google", "Google"),
    )
    email           = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified     = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    provider        = models.CharField(max_length=20,choices=PROVIDER, default=PROVIDER[0][0])

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = []

    objects         = UserManager()

    def __str__(self) -> str:
        return self.email

    def token(self):
        token = RefreshToken.for_user(self)
        return {
            "access_token":str(token.access_token),
            "refresh":str(token)
        }

class BasicDetails(models.Model):
    first_name          = models.CharField(max_length=30)
    last_name           = models.CharField(max_length=30)
    mobile_number       = models.CharField(max_length=25, default=None, null=True, blank=True)
    is_number_verified  = models.BooleanField(default=False)
    is_number_public    = models.BooleanField(default=False)
    notification_via_wa = models.BooleanField(default=False)
    location            = models.CharField(max_length=20, default=None, null=True, blank=True)
    headline            = models.TextField(default=None, null=True, blank=True)
    profile_summary     = models.TextField(default=None, null=True, blank=True)
    user                = models.OneToOneField("User", on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return "%s %s"%(self.first_name, self.last_name)