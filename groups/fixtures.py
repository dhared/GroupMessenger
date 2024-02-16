from django.contrib.auth import get_user_model
from groups.models import Group
from chats.models import Chat


User = get_user_model()


def create_user(username='Test', **kwargs):
    return User.objects.create(
        username=username,
        **kwargs,
    )


def create_group(name='Test Group', **kwargs):
    return Group.objects.create(
        name=name,
        **kwargs
    )


def add_member_to_group(group, user):
    group.members.add(user)


def create_chat(text='Hello', group=None, **kwargs):
    if not group:
        group = create_group()

    return Chat.objects.create(
        text=text,
        group=group,
        **kwargs
    )
