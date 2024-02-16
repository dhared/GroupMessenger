from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from groups import fixtures
from groups.models import Group

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


class GroupTestCase(BaseApiTestCase):

    def test_list(self):
        fixtures.create_group('Test Group 1')
        group2 = fixtures.create_group('Test Group 2')

        fixtures.add_member_to_group(group2, self.user)
        path = reverse('group-list')
        auth_headers = self.get_authentication_header()
        response = self.client.get(path, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], group2.id)
        self.assertEqual(response.data[0]['name'], group2.name)

    def test_create(self):
        data = {
            "name": "My Group"
        }
        path = reverse('group-list')
        auth_headers = self.get_authentication_header()
        response = self.client.post(path, data=data, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.data, {
            **data,
            "id": 1,
            "created_by": self.user.id,
            "members": [self.user.id],
        })
        groups = Group.objects.filter(name=data['name'])
        self.assertEqual(groups.count(), 1)

    def test_update(self):
        group = fixtures.create_group()
        fixtures.add_member_to_group(group, self.user)
        data = {
            "name": "My Group"
        }
        path = reverse('group-detail', kwargs={'pk': group.pk})
        auth_headers = self.get_authentication_header()
        response = self.client.patch(path, data=data, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {
            **data,
            "id": group.id,
            "created_by": group.created_by,
            "members": [self.user.id],
        })

    def test_delete(self):
        group = fixtures.create_group()
        fixtures.add_member_to_group(group, self.user)
        path = reverse('group-detail', kwargs={"pk": group.pk})
        auth_headers = self.get_authentication_header()
        response = self.client.delete(path, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Group.objects.filter(id=group.id).exists())

    def test_add_member(self):
        group = fixtures.create_group()
        fixtures.add_member_to_group(group, self.user)
        user = fixtures.create_user('iam')
        data = {
            "users": [user.id],
        }
        path = reverse('group-member', kwargs={"pk": group.pk})
        auth_headers = self.get_authentication_header()
        response = self.client.post(path, data=data, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(group.members.filter(id=user.id).exists())

    def test_remove_member(self):
        group = fixtures.create_group()
        user = fixtures.create_user('iam')
        fixtures.add_member_to_group(group, self.user)
        fixtures.add_member_to_group(group, user)
        data = {
            "users": [user.id],
        }
        path = reverse('group-member', kwargs={"pk": group.pk})
        auth_headers = self.get_authentication_header()
        response = self.client.delete(path, data=data, headers=auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(group.members.filter(id=user.id).exists())
