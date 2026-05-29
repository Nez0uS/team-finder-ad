from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
from .utils import generate_avatar


MAX_NAME_LENGTH = 124
MAX_SURNAME_LENGTH = 124
MAX_PHONE_LENGTH = 12
MAX_ABOUT_LENGTH = 256


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    surname = models.CharField(max_length=MAX_SURNAME_LENGTH)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(
        max_length=MAX_PHONE_LENGTH, unique=True, blank=True, null=True
    )
    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(
        max_length=MAX_ABOUT_LENGTH, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = generate_avatar(self)
        super().save(*args, **kwargs)
