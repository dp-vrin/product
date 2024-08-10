"""Admin file for reguster model."""
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "is_active")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "created_at", "updated_at")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_editable = ["username"]
    list_display = (
        "id",
        "email",
        "username",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email", "first_name", "last_name", "username")
    ordering = ("email", "username")
    # readonly_fields = ("created_at", "updated_at")


# Now register the new UserAdmin...
admin.site.register(CustomUser, CustomUserAdmin)
