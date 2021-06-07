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
        Profile.objects.create(**self.profile_data)

    def test_registration(self):
        response = self.client.post('/blog/user/register/', self.register_data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'blog_index.html')

    def test_login(self):
        response = self.client.post('/blog/user/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/blog/')
