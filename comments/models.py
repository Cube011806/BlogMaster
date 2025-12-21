from django.db import models
from posts.models import Post
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Komentarz {self.id} do {self.post.title}"
