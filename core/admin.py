# Register your models here.
from django.contrib import admin
from .models import Course, StudentProfile, Post, Comment,UserRole

admin.site.register(Course)
admin.site.register(StudentProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserRole)


