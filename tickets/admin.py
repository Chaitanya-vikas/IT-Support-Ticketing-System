from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Ticket

# 1. Register the Ticket model so you can see/edit tickets
admin.site.register(Ticket)

# 2. Register your Custom User model
# We extend the standard UserAdmin so it still looks like a user manager
class CustomUserAdmin(UserAdmin):
    # This adds our custom fields to the admin page
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {'fields': ('is_customer', 'is_support')}),
    )

admin.site.register(User, CustomUserAdmin)