from django.contrib import admin

from publishings.models import Profile, Subscription


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'avatar', 'content', 'is_paid', 'subscribe',)
    list_filter = ('is_paid',)
    search_fields = ('first_name', 'last_name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'status', 'stripe_customer_id', 'subscription_id', 'is_active',)
