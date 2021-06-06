from django.contrib.auth.models import User
from django.test import TestCase


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

    def test_registration(self):
        response = self.client.post('/blog/user/register/', self.register_data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'blog_index.html')

    def test_login(self):
        User.objects.create_user(**self.credentials)
        response = self.client.post('/blog/user/login/', **self.credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
