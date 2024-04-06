from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User


# https://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        ("Custom fields", {"fields": ("email_is_verified",)}),
    )


admin.site.register(User, MyUserAdmin)
