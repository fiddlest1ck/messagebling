from django.contrib import admin
from app.models import Message, Attachment, Notification

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)

class AttachmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attachment, AttachmentAdmin)

class NotificationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notification, NotificationAdmin)