from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        
        email = self.normalize_email(email)
        extra_fields.setdefault('role', 'guest')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    class PermissionType(models.TextChoices):
        CREATE = 'create', 'ایجاد محتوا'
        EDIT = 'edit', 'ویرایش محتوا'
        DELETE = 'delete', 'حذف محتوا'
        MANAGE_USERS = 'manage', 'مدیریت کاربران'
    
    class RoleChoices(models.TextChoices):
        VIEWER = 'viewer', 'مشاهده‌کننده'
        EDITOR = 'editor', 'ویرایشگر'
        ADMIN = 'admin', 'مدیر سیستم'
        

    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    role = models.CharField(
        max_length=50,
        choices=RoleChoices.choices,
        default='guest'
    )
    
    permissions = models.CharField(max_length=100, blank=True)

    def get_permissions_list(self):
        return self.permissions.split(',') if self.permissions else []

    def set_permissions(self, items):
        self.permissions = ','.join(items)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name'],
                name='unique_full_name'
            )
        ]
    
    @property
    def is_editor(self):
        return 'edit' in self.permissions
    
    @property
    def is_creator(self):
        return 'create' in self.permissions

    @property
    def is_manager(self):
        return 'manage' in self.permissions

    @property
    def is_deletor(self):
        return 'delete' in self.permissions
    