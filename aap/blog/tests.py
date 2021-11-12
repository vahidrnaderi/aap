"""Blog tests."""
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from blog.models import Tag


class BlogTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('blog/', include('blog.urls')),
    ]

    def test_create_tag(self):
        """
        Ensure we can create a tag.
        """
        url = reverse('tag-list')
        # url = 'http://127.0.0.1:8000/blog/tags/'
        data = {'name': 'test'}
        response = self.client.post(url, data, format='json')
        # self.client.credentials(HTTP_AUTHORIZATION='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        # self.client.credentials(Authorization='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'DabApps')

    def test_get_all_tags(self):
        """
        Ensure we can retrieve all tags.
        """
        # url = reverse('tag')
        url = 'http://127.0.0.1:8000/blog/tags/'
        # response = self.client.post(url, data, format='json')
        response = self.client.get(url)
        # self.client.credentials(Authorization='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
