from django.db import models
from blogs.models import Blog
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    def __str__(self):
        return self.title

class PostVisit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="visits")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Odwiedziny: {self.post.title} ({self.created_at})"
