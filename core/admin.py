# Register your models here.
from django.contrib import admin
from .models import Course, Post, Comment, UserProfile, ChatMessage

admin.site.register(Course)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(ChatMessage)
