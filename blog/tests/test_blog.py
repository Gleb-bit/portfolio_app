from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Post, Category, Profile


class TestBlog(TestCase):
    @classmethod
    def setUp(self):
        self.credentials = {
            'username': 'admin',
            'password': 'admin'
        }

        self.user_comment_data = {
            'author': 'admin',
            'body': 'nothing'
        }
        self.user_edit_comment_data = {
            'author': 'someone',
            'body': 'something'
        }
        self.user_post_data = {
            'title': 'First',
            'body': 'anything',
            'categories': 'test'
        }
        self.edit_user_post_data = {
            'title': 'First',
            'body': 'anything',
            'categories': 'test another_test'
        }
        user = User.objects.create_user(**self.credentials)
        self.profile_data = {
            'user': user,
            'name': 'Johnny',
            'surname': 'Depp',
        }
        profile = Profile.objects.create(**self.profile_data)
        category = Category.objects.create(name='anything')
        post = Post.objects.create(title='title', body='body', profile=profile)
        post.categories.set([category])

    def test_create_comment(self):
        response = self.client.post('/blog/1/', self.user_comment_data)
        self.assertEqual(response.context['comments'][0].author, self.user_comment_data['author'])
        self.assertEqual(response.context['comments'][0].body, self.user_comment_data['body'])

    def test_edit_comment(self):
        self.client.post('/blog/1/', self.user_comment_data)
        response = self.client.post('/blog/edit/comment/1/', self.user_edit_comment_data)
        self.assertRedirects(response, '/blog/1/')

    def test_create_post(self):
        self.client.login(**self.credentials)
        response = self.client.post('/blog/create/post', self.user_post_data, follow=True)
        self.assertRedirects(response, '/blog/')

    def test_edit_post(self):
        self.client.login(**self.credentials)
        response = self.client.post('/blog/edit/post/1/', self.user_post_data, follow=True)
        self.assertRedirects(response, '/blog/1/')
