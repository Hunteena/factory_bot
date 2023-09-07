from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import User, Message

admin.site.register(User, UserAdmin)
admin.site.register(Message)
