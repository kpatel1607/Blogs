from datetime import timezone
from rest_framework import serializers
from .models import User, Blog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

class BlogSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Create and return a new Blog instance using the validated data
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update the Blog instance with the validated data
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.author = validated_data.get('author', instance.author)
        instance.updated_at = timezone.now()  # Update the timestamp
        instance.save()
        return instance
