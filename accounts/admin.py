from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, Team
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("None", {"fields": ("email", "role", "team")}),  # comma required
    )
    fieldsets = UserAdmin.fieldsets + (("None", {"fields": ("role", "team")}),)
    list_display = [
        "username",
        "email",
        "last_name",
        "first_name",
        "role",
        "team",
        "is_staff",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Team)
