from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from django.contrib.auth.models import Group


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False, verbose_name='Is Member')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name = 'Creation Date')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"




class CustomGroup(Group):

    # Add custom fields or methods here
    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"


