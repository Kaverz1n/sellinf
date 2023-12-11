from django.contrib.auth.models import Permission, Group
from django.core.cache import caches
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from content.models import Content

from users.models import User


class TestContent(TestCase):
    '''
    Content test case
    '''

    def setUp(self) -> None:
        call_command('flush', interactive=False)
        caches['default'].clear()

        # user set up
        users_data = (
            {
                'id': 1,
                'phone': '+1',
                'nickname': 'Admin',
                'password': 'Admin',
                'is_upgraded': True,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            },
            {
                'id': 2,
                'phone': '+2',
                'nickname': 'Moderator',
                'password': 'Moderator',
                'is_upgraded': True,
                'is_staff': True,
                'is_superuser': False,
                'is_active': True
            },
            {
                'id': 3,
                'phone': '+3',
                'nickname': 'User',
                'password': 'User',
                'is_upgraded': False,
                'is_staff': False,
                'is_superuser': False,
                'is_active': True
            },
        )

        User.objects.bulk_create(User(**user_data) for user_data in users_data)

        self.admin, self.moderator, self.user = User.objects.all()

        group, created = Group.objects.get_or_create(name='moderator')
        self.moderator.groups.add(group)

        # content set up
        content_data = {
            'id': 2,
            'owner': self.admin,
            'title': 'test',
            'content': 'test',
            'type': 'premium',
        }

        self.content = Content.objects.create(**content_data)

    def test_index(self) -> None:
        response = self.client.get(reverse('content:index'))

        self.assertEqual(
            response.status_code,
            200
        )

    def test_content_list_view(self):
        response = self.client.get(reverse('content:content_list'))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('content:content_list'))

        self.assertEqual(
            response.status_code,
            200
        )

    def test_found_content_list(self):
        response = self.client.get(reverse('content:found_content_list', kwargs={'search_query': 'test1'}))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('content:found_content_list', kwargs={'search_query': 'test1'}))

        self.assertEqual(
            response.status_code,
            200
        )

    def test_user_content_list(self):
        response = self.client.get(reverse('content:user_content_list', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.moderator)

        response = self.client.get(reverse('content:user_content_list', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            302
        )

    def test_moderator_content_list(self):
        response = self.client.get(reverse('content:moderator_content_list'))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('content:moderator_content_list'))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.logout()
        self.client.force_login(self.moderator)

        response = self.client.get(reverse('content:moderator_content_list'))

        self.assertEqual(
            response.status_code,
            200
        )

    def test_content_detail(self):
        response = self.client.get(reverse('content:content_detail', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.admin)

        response = self.client.get(reverse('content:content_detail', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            200
        )

    def test_content_create(self):
        response = self.client.get(reverse('content:content_create'))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('content:content_create'))

        self.assertEqual(
            response.status_code,
            302
        )

        permission = Permission.objects.get(codename='add_content')
        self.user.user_permissions.add(permission)

        response = self.client.get(reverse('content:content_create'))

        self.assertEqual(
            response.status_code,
            200
        )

        response = self.client.post(
            reverse('content:content_create'),
            data={
                'title': 'Test2',
                'content': 'test2',
                'type': 'free'
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            len(Content.objects.all()),
            2
        )

    def test_content_update(self):
        response = self.client.get(reverse('content:content_update', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('content:content_update', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            302
        )

        permission = Permission.objects.get(codename='add_content')
        self.user.user_permissions.add(permission)

        response = self.client.get(reverse('content:content_update', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.logout()
        self.client.force_login(self.admin)

        permission = Permission.objects.get(codename='change_content')
        self.user.user_permissions.add(permission)

        response = self.client.get(reverse('content:content_update', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            200
        )

        response = self.client.post(
            reverse('content:content_update', kwargs={'pk': 2}),
            data={
                'title': 'testtest',
                'content': 'testtest',
                'type': 'free'
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            'testtest',
            Content.objects.get(pk=2).title
        )

    def test_content_delete(self):
        response = self.client.get(reverse('content:content_delete', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('content:content_update', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            302
        )

        permission = Permission.objects.get(codename='add_content')
        self.user.user_permissions.add(permission)

        response = self.client.get(reverse('content:content_update', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.logout()
        self.client.force_login(self.admin)

        permission = Permission.objects.get(codename='delete_content')
        self.user.user_permissions.add(permission)

        response = self.client.get(reverse('content:content_update', kwargs={'pk': 2}))

        self.assertEqual(
            response.status_code,
            200
        )

        response = self.client.post(
            reverse('content:content_delete', kwargs={'pk': 2})
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            0,
            len(Content.objects.all())
        )

    def test_about(self):
        response = self.client.get(reverse('content:about'))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('content:about'))

        self.assertEqual(
            response.status_code,
            200
        )

    def test_upgrade(self):
        response = self.client.get(reverse('content:upgrade'))

        self.assertEqual(
            response.status_code,
            302
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('content:upgrade'))

        self.assertEqual(
            response.status_code,
            200
        )
