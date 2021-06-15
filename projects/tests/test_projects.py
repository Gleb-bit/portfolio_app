from django.test import TestCase


class TestProjects(TestCase):

    def test_list_projects(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_project.html')
