from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list = ['title', 'description', 'image']


admin.site.register(Post)
