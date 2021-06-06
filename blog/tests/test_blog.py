from django.test import TestCase

from blog.models import Post, Category


class TestBlog(TestCase):
    @classmethod
    def setUp(self):
        self.user_data = {
            'author': 'anonim',
            'body': 'nothing'
        }
        category = Category.objects.create(name='anything')
        post = Post.objects.create(title='title', body='body')
        post.categories.set([category])

    def test_comment(self):
        response = self.client.post('/blog/1/', self.user_data)
        self.assertEqual(response.status_code, 200)
