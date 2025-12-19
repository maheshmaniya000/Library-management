from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.base_user import BaseUserManager


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, mobile_number=None, password=None, **extra_fields):
        if extra_fields.get('is_superuser', False)==False:
            if not email and not mobile_number:
                raise ValueError("The given email or mobile number must be set")
        if email:
            email = self.normalize_email(email)
            extra_fields['email'] = email
        
        if mobile_number:
            extra_fields['mobile_number'] = mobile_number
        
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, mobile_number=None, password=None, **extra_fields):
        return self._create_user(email, mobile_number, password, **extra_fields)

    def create_superuser(self, email=None, mobile_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)        
        return self._create_user(email, mobile_number, password, **extra_fields)



class User(AbstractUser, Base):
    """Custom User model with role-based access""" 
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    def __str__(self):
        return self.username

    
