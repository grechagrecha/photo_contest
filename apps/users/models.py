from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core import exceptions
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill, Anchor


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

        group, created = Group.objects.get_or_create(name='Customers')
        user.groups.add(group)

        return user

    def create_superuser(self, username, email, password=None):
        superuser = self.create_user(username, email, password)

        superuser.is_superuser = True
        superuser.is_staff = True

        superuser.role = superuser.Roles.ADMIN
        admin_group, created = Group.objects.get_or_create(name='Admins')
        customer_group, created = Group.objects.get_or_create(name='Customers')
        customer_group.user_set.remove(superuser)
        superuser.groups.add(admin_group)

        superuser.save()

        return superuser


class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=self.model.Roles.CUSTOMER)

    def create_superuser(self, username, email, password=None):
        return exceptions.PermissionDenied('To create a superuser use the User model.')


class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'

    objects = UserManager()

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    avatar = models.ImageField(upload_to='images/avatars/', blank=True)
    avatar_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(width=360, height=360, anchor=Anchor.CENTER)],
        format='JPEG',
        options={'quality': 60}
    )
    role = models.CharField(choices=Roles.choices, default=Roles.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    token = models.CharField(max_length=256, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.role}: {self.username}'


class Customer(User):
    class Meta:
        proxy = True

    objects = CustomerManager()
