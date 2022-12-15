import json

from django.contrib import admin

from .models import PushInformation, SubscriptionInfo
from .utils import _send_notification
from django.urls import reverse
from django.utils.html import format_html


class PushInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "subscription_link", "group_name")
    actions = ("send_test_message",)

    def send_test_message(self, request, queryset):
        payload = {"head": "Hey", "body": "Hello World"}
        for device in queryset:
            notification = _send_notification(device.subscription, json.dumps(payload), 0)
            if notification:
                self.message_user(request, "Test sent successfully")
            else:
                self.message_user(request, "Deprecated subscription deleted")

    def subscription_link(self, obj):
        try:
            href = reverse('admin:webpush_subscriptioninfo_change', kwargs={'object_id':obj.subscription.id})
            link = format_html(f'<a href="{href}">{obj.subscription.browser}:{obj.subscription.auth}</a>')
        except Exception as e:
            print("error", e)
            link = ''
        return link

admin.site.register(PushInformation, PushInfoAdmin)

class SubscriptionInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "browser", "auth", "p256dh")

admin.site.register(SubscriptionInfo, SubscriptionInfoAdmin)
