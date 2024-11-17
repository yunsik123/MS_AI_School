import uuid

from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission

from django.db import models

from ai.models import ModelManager, BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    # REQUIRED_FIELDS = 'phone_number',
    USERNAME_FIELD = 'username'

    def __str__(self):
        return '{} ({})'.format(self.username, self.name)

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = verbose_name

    username = models.EmailField(max_length=50, unique=True, verbose_name='이메일')
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='이름')
    phone_number = models.CharField(max_length=15, null=True, verbose_name='전화번호')

    signup_date = models.DateTimeField(verbose_name='SignUp Date', default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    agree_push = models.BooleanField(null=True, verbose_name='푸시알림 동의')

    groups = models.ManyToManyField(Group, related_name='users', blank=True, null=True)
    user_permissions = models.ManyToManyField(Permission, related_name='users', blank=True, null=True)

    objects = UserManager()
