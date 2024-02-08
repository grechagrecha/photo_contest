from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if username is None:
            raise TypeError('User must have a username')
        if email is None:
            raise TypeError('User must have an email adress')
        if password is None:
            raise TypeError('User must have a password')

        user = self.model(username=username, email=self.normalize_email(email))
        user.role = user.Roles.CUSTOMER
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):
        superuser = self.create_user(username, email, password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.role = superuser.Roles.ADMIN
        superuser.save()

        return superuser


class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=self.model.Roles.CUSTOMER)


class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'

    objects = UserManager()

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    avatar = models.ImageField(upload_to='images/avatars/')
    role = models.CharField(choices=Roles.choices, default=Roles.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    token = models.CharField(max_length=256)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.role}: {self.username}'


class Customer(User):
    class Meta:
        proxy = True

    objects = CustomerManager()
