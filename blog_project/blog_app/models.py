from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    # blogs = models.(Blog, on_delete=models.CASCADE, related_name="blogs")

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
