from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

admin.site.register(Permission)

class CredentialsAdmin(admin.ModelAdmin):
    list_display = ('file_name',)

    def file_name(self, obj):
        return obj.credentials.name.split('/')[-1]  # Display the filename
    file_name.short_description = 'File Name'

    def get_readonly_fields(self, request, obj=None):
        """Make 'credentials' field readonly in the admin form after saving the object."""
        if obj:
            return self.readonly_fields + ('credentials',)
        return self.readonly_fields

admin.site.register(Credentials, CredentialsAdmin)



@admin.register(SoftwarePermissions)
class SoftwarePermissionsAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    list_filter = ('permissions',)
    fieldsets = (
        (None, {
            'fields': ('user', 'permissions')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request)

@admin.register(SMTPConfiguration)
class SMTPConfigurationAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('user','host', 'port', 'secure', 'auth_user', 'is_secure_display')
    list_filter = ('user','secure')  # Filter options for SSL/TLS
    search_fields = ('user','host', 'auth_user')  # Enable search functionality
    ordering = ('user',)  # Default ordering by host

    # Fields to display in the form view
    fieldsets = (
        ('SMTP Server Details', {
            'fields': ('user','host', 'port', 'secure'),
            'description': "Enter the details for your SMTP server."
        }),
        ('Authentication', {
            'fields': ('auth_user', 'auth_password'),
            'description': "Provide the credentials for SMTP authentication."
        }),
    )

    # Customize the admin form behavior
    def is_secure_display(self, obj):
        return "Yes" if obj.secure else "No"
    is_secure_display.short_description = "Uses SSL/TLS"


@admin.register(EmailAccounts)
class EmailAccountsAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'expiry_time')
    search_fields = ('email',)
    list_filter = ('user',)
    ordering = ('email',)

@admin.register(AudienceData)
class AudienceDataAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'tag')
    search_fields = ('email','tag')
    list_filter = ('user','tag')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'user')
    search_fields = ('tag_name',)
    list_filter = ('user',)

@admin.register(tags_data)
class TagsDataAdmin(admin.ModelAdmin):
    list_display = ('tag', 'data','user')
    search_fields = ('data','user')
    list_filter = ('tag','user')

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user','format_type', 'sender_name')
    search_fields = ('subject', 'content','format_type')
    list_filter = ('user','format_type')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'ip_address', 'audience_data', 'send_from','date_time')
    search_fields = ('ip_address', 'user__username')
    list_filter = ('status', 'date_time','audience_data', 'send_from')
    ordering = ('-date_time',)

# Inline Configurations
class TagsDataInline(admin.TabularInline):
    model = tags_data
    extra = 1

class TagsAdminWithInline(TagsAdmin):
    inlines = [TagsDataInline]

# Admin overrides for inline demonstration
admin.site.unregister(Tags)
admin.site.register(Tags, TagsAdminWithInline)

@admin.register(SiteSettings)
class SiteIconAdmin(admin.ModelAdmin):
    list_display = ('icon_preview','login_image_preview')

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" alt="{}">',
                obj.icon.url,
                'icon',
            )
        return "No Icon"
    def login_image_preview(self, obj):
        if obj.login_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" alt="{}">',
                obj.login_image.url,
                'Login',
            )
        return "No Login Image"
    icon_preview.short_description = "Login Image"


admin.site.site_header = "API SHOOTER"
admin.site.site_title = "API SHOOTER"
admin.site.index_title = "API SHOOTER"
