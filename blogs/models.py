from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class BlogCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(BlogCategory, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='images/', null=True, blank=True) 
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title
