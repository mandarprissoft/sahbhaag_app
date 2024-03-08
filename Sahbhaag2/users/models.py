from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=50, default='')
    age = models.IntegerField(default=0)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    address = models.TextField()
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    center = models.ForeignKey('Center', on_delete=models.CASCADE, default=1)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    year_of_experience = models.IntegerField(default=0)
    training_type = models.CharField(max_length=100, default='', blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fees_paid = models.CharField(max_length=10, default='', blank=True)
    first_login = models.BooleanField(default=True)
    token = models.CharField(max_length=500, default='', blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        related_query_name='custom_user_group',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        related_query_name='custom_user_permission',
        blank=True
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    # @property
    # def id(self):
    #     return self.user_id

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # def get_unique_identifier(self):
    #     return self.username

    def __str__(self):
        return f"{self.username} - {self.role}"

class Role(models.Model):
    role_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.role_type}"


class Center(models.Model):
    center_name = models.CharField(max_length=100)
    address =  models.TextField()
# Create your models here.
