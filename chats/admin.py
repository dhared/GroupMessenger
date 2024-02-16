from django.contrib import admin

from chats.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass
