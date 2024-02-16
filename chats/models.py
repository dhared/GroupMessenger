from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F


User = get_user_model()


class Chat(models.Model):
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False)
    likes = models.ManyToManyField(User, blank=True)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_like(self, user: User):
        if self.likes.filter(id=user.id).exists():
            return
        self.likes.add(user)
        self.likes_count = F('likes_count') + 1
        self.save()
        self.refresh_from_db()

    def remove_like(self, user: User):
        if not self.likes.filter(id=user.id).exists():
            return
        self.likes.remove(user)
        self.likes_count = F('likes_count') - 1
        self.save()
        self.refresh_from_db()
