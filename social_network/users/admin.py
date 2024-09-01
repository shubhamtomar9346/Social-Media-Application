from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, FriendRequest


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model in the admin panel.
    list_display = ('email', 'username', 'is_staff', 'is_active')  # Customize the fields you want to display

    # Fields to filter the results by in the right sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Fieldsets define the layout of the admin "edit" page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Add fields to be used in the User creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    # Allowing user deletion
    actions = ['delete_selected']

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        queryset.delete()


# Register the custom User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)  # Optional: Unregister Group if you don't need it in the admin panel


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = ('id', 'from_user', 'to_user', 'is_accepted', 'timestamp')

    # Add search functionality for users
    search_fields = ('from_user__username', 'to_user__username', 'from_user__email', 'to_user__email')

    # Add filters for accepted status and timestamp
    list_filter = ('is_accepted', 'timestamp')

    # Order the list by the 'id' field by default
    ordering = ('id',)

    # Optionally, you can define fields to be displayed in the detail view
    fields = ('id', 'from_user', 'to_user', 'is_accepted', 'timestamp')

    # Make the 'id' field read-only, as it is auto-generated
    readonly_fields = ('id', 'timestamp')
