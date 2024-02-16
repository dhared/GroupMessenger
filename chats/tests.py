from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from chats.models import Chat
from groups import fixtures


User = get_user_model()


class BaseApiTestCase(APITestCase):
    def setUp(self):
        self.user = fixtures.create_user()
        self.user.set_password('xyz#Dq45refd')

    def get_authentication_header(self):
        token = RefreshToken.for_user(self.user)
        return {
            "Authorization": f"Bearer {token.access_token}"
        }


class ChatTestCase(BaseApiTestCase):
    def setUp(self):
        super().setUp()
        self.group = fixtures.create_group()
        fixtures.add_member_to_group(self.group, self.user)

    def test_list(self):
        fixtures.create_chat('This is other group chat')
        chat = fixtures.create_chat('This is my group chat', group=self.group)
        path = reverse('chat-list')
        auth_headers = self.get_authentication_header()
        response = self.client.get(path, headers=auth_headers)
        # breakpoint()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], chat.id)
        self.assertEqual(response.data[0]['text'], chat.text)
        self.assertEqual(response.data[0]['group'], chat.group_id)
        self.assertEqual(response.data[0]['likes_count'], chat.likes_count)

    def test_create(self):
        data = {
            "text": "Hi there",
            "group": self.group.id
        }
        path = reverse('chat-list')
        auth_headers = self.get_authentication_header()
        response = self.client.post(path, data=data, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['text'], data['text'])
        self.assertEqual(response.data['group'], data['group'])
        self.assertEqual(response.data['likes_count'], 0)

        chats = Chat.objects.filter(group=self.group)
        self.assertEqual(len(chats), 1)
        self.assertEqual(chats[0].text, data['text'])

    def test_update(self):
        chat = fixtures.create_chat(text='Hiiii', group=self.group)
        data = {
            "text": "Hi there"
        }
        path = reverse('chat-detail', kwargs={"pk": chat.pk})
        auth_headers = self.get_authentication_header()
        response = self.client.patch(path, data=data, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['text'], data['text'])
        self.assertEqual(response.data['group'], chat.group_id)
        self.assertEqual(response.data['likes_count'], 0)

        chats = Chat.objects.filter(group=self.group)
        self.assertEqual(len(chats), 1)
        self.assertEqual(chats[0].text, data['text'])

    def test_delete(self):
        chat = fixtures.create_chat(group=self.group)
        path = reverse('chat-detail', kwargs={"pk": chat.pk})
        auth_headers = self.get_authentication_header()
        response = self.client.delete(path, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Chat.objects.filter(id=chat.id).exists())

    def test_add_like(self):
        chat = fixtures.create_chat(group=self.group)
        self.assertEqual(chat.likes_count, 0)

        path = reverse('chat-like', kwargs={"pk": chat.pk})
        auth_headers = self.get_authentication_header()
        response = self.client.post(path, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        chat.refresh_from_db()
        self.assertEqual(chat.likes_count, 1)

    def test_remove_like(self):
        chat = fixtures.create_chat(group=self.group)
        chat.add_like(self.user)
        self.assertEqual(chat.likes_count, 1)

        path = reverse('chat-like', kwargs={"pk": chat.pk})
        auth_headers = self.get_authentication_header()
        response = self.client.delete(path, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        chat.refresh_from_db()
        self.assertEqual(chat.likes_count, 0)
