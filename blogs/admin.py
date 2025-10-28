from django.contrib import admin
from .models import Blog, Post

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'blog', 'created_at')
    search_fields = ('title', 'content')