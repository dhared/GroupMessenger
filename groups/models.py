from typing import List

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=125)
    members = models.ManyToManyField(User, related_name='joined_groups', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}'

    def add_members(self, users: List[User]):
        assert len(users) > 0
        self.members.add(*users)

    def remove_members(self, users: List[User]):
        assert len(users) > 0
        self.members.remove(*users)
