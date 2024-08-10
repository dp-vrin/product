# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class UserType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.name = (self.name).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    """Custom user manager for CustomUser."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)  # Ensure user is active
        extra_fields.setdefault("is_admin", True)  # Ensure superuser is active

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model."""

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        _("username"), max_length=20, null=True, blank=True, unique=True
    )
    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(_("admin"), default=False)
    user_type = models.ForeignKey(
        UserType,
        null=True,
        on_delete=models.SET_NULL,
        related_name="custom_user_type",
    )
    permissions = models.ManyToManyField(Permission, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def type_of_user(self):
        if self.user_type:
            return (self.user_type.name).upper()
        return None

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        """Return the email when printing a user object."""
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
