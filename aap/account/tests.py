"""Account tests."""
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from blog.models import User


class AccountTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('account/', include('account.urls')),
    ]

    def __user_signup(self, username, password, email):
        url = 'http://127.0.0.1:8000/account/register/'
        data = {'username': username, 'email': email, 'password': password}
        return self.client.post(url, data, format='json')

    def test_register_user(self):
        """
        Ensure we can register a user.
        """
        # url = reverse('tag')
        # url = 'http://127.0.0.1:8000/account/register/'
        # data = {'username': 'vrn', 'email': 'aa@aa.com', 'password': 't12345'}
        # response = self.client.post(url, data, format='json')
        response = self.__user_signup('vrn', 't12345', 'aa@aa.com')
        # self.client.credentials(HTTP_AUTHORIZATION='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        # self.client.credentials(Authorization='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        # print(User.objects.all())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'vrn')

    def test_login_user(self):
        """
        Ensure user can login.
        """
        # url = reverse('tag')
        response = self.__user_signup('vrn', 't12345', 'aa@aa.com')
        url = 'http://127.0.0.1:8000/account/login/'
        data = {'username': 'vrn', 'password': 't12345'}
        response = self.client.post(url, data, format='json')
        print(data)
        print(User.objects.all())
        print(response)
        # import pdb; pdb.set_trace()

        # response = self.client.post(url, data, format='json')
        # response = self.client.get(url)
        # self.client.credentials(Authorization='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_all_users(self):
    #     """
    #     Ensure we can retrieve all users.
    #     """
    #     # url = reverse('tag')
    #     url = 'http://127.0.0.1:8000/account/users/'
    #     # response = self.client.post(url, data, format='json')
    #     response = self.client.get(url)
    #     # self.client.credentials(Authorization='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
