from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PoolUser

class PoolUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {
        'fields':  ('is_subscribed',)
    }),)

admin.site.register(PoolUser, PoolUserAdmin)
