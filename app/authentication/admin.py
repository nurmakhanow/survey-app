from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from app.authentication.forms import UserChangeForm, UserCreationForm


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active')}),
        ('Change password', {'fields': ('password1', 'password2')}),
        ('Permissions', {'fields': ('is_superuser', 'is_admin')}),
    )
    list_display = ("email", "is_superuser")
    list_filter = ('is_active', 'is_superuser')
    search_fields = ["email"]
    ordering = ('id',)
    filter_horizontal = ()
