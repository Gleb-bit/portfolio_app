from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Profile


class TestUser(TestCase):
    @classmethod
    def setUp(self):
        self.credentials = {
            'username': 'admin',
            'password': 'admin'
        }
        self.register_data = {
            'username': 'user',
            'name': 'admin',
            'surname': 'admin',
            'password1': 'dhf913r7nfydsf389r29',
            'password2': 'dhf913r7nfydsf389r29'
        }
        user = User.objects.create_user(**self.credentials)
        self.profile_data = {
            'user': user,
            'name': 'Johnny',
            'surname': 'Depp',
        }
        self.profile_edit_data = {
            'name': 'Brad',
            'surname': 'Pitt',
            'about_me': 'nothing'
        }
        Profile.objects.create(**self.profile_data)

    def test_registration(self):
        response = self.client.post('/blog/user/register/', self.register_data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'list_post.html')

    def test_login(self):
        response = self.client.post('/blog/user/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/blog/')

    def test_logout(self):
        self.client.login(**self.credentials)
        response = self.client.post('/blog/user/logout/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/blog/')

    def test_detail_account(self):
        self.client.login(**self.credentials)
        response = self.client.get('/blog/user/1')
        self.assertTemplateUsed(response, 'detail_account.html')

    def test_edit_account(self):
        self.client.login(**self.credentials)
        response = self.client.post('/blog/user/1/edit?', self.profile_edit_data)
        self.assertRedirects(response, '/blog/user/1')
