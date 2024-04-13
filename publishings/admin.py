from django.contrib import admin

from publishings.models import Profile, Subscription


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'avatar', 'content', 'is_status', 'user',)
    list_filter = ('is_status',)
    search_fields = ('first_name', 'last_name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'created_at', 'status', 'profile',)
