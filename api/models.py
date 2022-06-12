from django.db import models
from user.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class Caption(models.Model):
    text = models.TextField()
    media_url = models.URLField(max_length=1024)
    created = models.DateTimeField()
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Post(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    code = models.CharField(max_length=255)
    caption_data = models.ForeignKey(
        Caption,
        related_name="post_caption",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.code


class Feed(models.Model):
    # user = models.ForeignKey(User, related_name="user_feed", blank=False, null=False,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    posts = models.ManyToManyField(
        Post,
        related_name="feed_posts",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username
