from django.contrib import admin
from .models import User, Blog

# Register your models here
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')  # Display these fields in the list view

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')  # Display these fields in the list view
    search_fields = ('title', 'content')  # Add search functionality for title and content
    list_filter = ('author', 'created_at')  # Filter by author and created date
