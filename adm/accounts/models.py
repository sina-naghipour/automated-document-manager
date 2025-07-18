from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You have to set Email.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user








class CustomUser(AbstractUser):

    class PermissionType(models.TextChoices):
        CREATE = 'create', 'ایجاد محتوا'
        EDIT = 'edit', 'ویرایش محتوا'
        DELETE = 'delete', 'حذف محتوا'
        MANAGE_USERS = 'manage_users', 'مدیریت کاربران'
    
    
    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'مدیر سیستم'
        EDITOR = 'editor', 'ویرایشگر'
        VIEWER = 'viewer', 'مشاهده‌کننده'
        GUEST = 'guest', 'میهمان'


    username   = models.CharField(max_length=120, unique=True)
    email      = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name  = models.CharField(max_length=100)
    is_active  = models.BooleanField(default=True)

    role       = models.CharField(choices=RoleChoices.choices)
    permissions = models.CharField(max_length=100, blank=True)  # Stores "create,edit,delete"

    def get_permissions_list(self):
        return self.permissions.split(',') if self.permissions else []

    def set_permissions(self, items):
        self.permissions = ','.join(items)
    objects    = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    class Meta:
        
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name'], name='unique_full_name')
        ]

