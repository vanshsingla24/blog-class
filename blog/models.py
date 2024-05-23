from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """Model representing a tag for a blog."""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blog(models.Model):
    """Model representing a blog post."""
    title = models.CharField(unique=True, max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank='True')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_blogs', blank=True)


    def __str__(self):
        return self.title


class Comment(models.Model):
    """Model representing a comment on a blog."""
    blog = models.ForeignKey('Blog', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'
