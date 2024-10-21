import datetime
from .models import Blog, User
from django.core.cache import cache
from .serializers import BlogSerializer, UserSerializer
import json

# Fetch a blog by ID, with caching
def get_blog(blog_id):
    cached_blog = cache.get(f'blog_{blog_id}')
    if cached_blog:
        return cached_blog
    blog = Blog.objects.get(id=blog_id)
    cache.set(f'blog_{blog_id}', blog, timeout=60 * 5)  # Cache for 5 minutes
    return blog

# Fetch all blogs
def get_all_blogs():
    return Blog.objects.all()  # Fetch all blogs using Django ORM

# Create a new blog using the serializer
def create_blog_with_serializer(data):
    serializer = BlogSerializer(data=data)
    if serializer.is_valid():
        serializer.save()  # This will save the blog
        # Cache the newly created blog
        cache.set(f'blog_{serializer.instance.id}', serializer.instance, timeout=60 * 5)
        return serializer.instance
    return None, serializer.errors  # Return errors if not valid

# Update a blog using the serializer
def update_blog_with_serializer(blog_id, data):
    blog = get_blog(blog_id)
    serializer = BlogSerializer(blog, data=data)
    if serializer.is_valid():
        serializer.save()  # This will update the blog
        # Update cache
        cache.set(f'blog_{serializer.instance.id}', serializer.instance, timeout=60 * 5)
        return serializer.instance
    return None, serializer.errors  # Return errors if not valid

# Delete a blog
def delete_blog(blog_id):
    blog = Blog.objects.get(id=blog_id)
    cache.delete(f'blog_{blog_id}')  # Remove from cache
    blog.delete()

# Create a user using the serializer
def create_user_with_serializer(data):
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()  # This will save the user
        return serializer.instance
    return None, serializer.errors  # Return errors if not valid

# Fetch all users
def get_all_users():
    return User.objects.all()  # Fetch all users using Django ORM
