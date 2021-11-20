"""Account tests."""
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from blog.models import User


class AccountTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('account/', include('account.urls')),
    ]

    def __user_register(self, username, password, email, mobile):
        # print("222")
        # url = 'http://127.0.0.1:8000/account/register/'
        url = reverse('register')
        data = {'username': username, 'email': email, 'password': password, 'mobile': mobile}
        return self.client.post(url, data, format='json')

    def __user_login(self, username, password):
        url = reverse('login')
        # url = 'http://127.0.0.1:8000/account/login/'
        data = {'username': username, 'password': password}
        return self.client.post(url, data, format='json')

    def setUp(self):
        # print("111")
        # Create a user
        # self.test_user = self.__user_register('admin', 't12345', 'aa@aa.com', '09126084223')
        self.__user_register('admin', 't12345', 'aa@aa.com', '09126084223')
        # URL for creating user
        # self.create_url = reverse('user-create')

        # self.client = Client()
        # self.my_admin = User(username='user', is_staff=True)
        # my_admin.set_password('passphrase')  # can't set above because of hashing
        # my_admin.save()  # needed to save to temporary test db
        # response = self.client.get('/admin/', follow=True)
        # loginresponse = self.client.login(username='user', password='passphrase')
        # self.assertTrue(loginresponse)  # should now return "true"

    def test_1_register_user(self):
        """
        Ensure we can register a user.
        """
        url = reverse('register')
        # url = 'http://127.0.0.1:8000/account/register/'
        # data = {'username': 'vrn', 'email': 'aa@aa.com', 'password': 't12345'}
        # response = self.client.post(url, data, format='json')
        response = self.__user_register('vrn', 't12345', 'aa1@aa.com', '090107145')
        # self.client.credentials(HTTP_AUTHORIZATION='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        # self.client.credentials(Authorization='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        # print(f"1: {User.objects.all()}")
        # print(f"11: {list(User.objects.all().values_list('username', flat=True))}")
        # print(f"2: {User.objects.get().username}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='vrn').username, 'vrn')

    def test_2_login_user(self):
        """
        Ensure user can login.
        """
        response = self.__user_register('vrn', 't12345', 'aa@aa.com', '09126084222')
        print(response)

        # url = reverse('login')
        # # url = 'http://127.0.0.1:8000/account/login/'
        # data = {'username': 'admin', 'password': 't12345'}
        # response = self.client.post(url, data, format='json')
        response = self.__user_login('vrn', 't12345')
        # print(f"3: {data}")
        # print(f"4: {url}")
        # print(f"5: {User.objects.all()}")
        # print(f"6: {User.objects.get().username}")
        # print(f"7: {response}")
        # print(f"8: {list(response.data.keys())[0]}")
        # print(f"9: {response.content}")
        # import pdb; pdb.set_trace()

        # response = self.client.post(url, data, format='json')
        # response = self.client.get(url)
        # self.client.credentials(Authorization='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys())[0], 'token')

    def test_3_get_all_users(self):
        """
        Ensure we can retrieve all users.
        """
        response = self.__user_login('admin', 't12345')
        print(f"\n{response.data['token']}")
        # self.client.credentials(Authorization='token ' + response.data['token'])

        # user = User.objects.get(username='admin')
        # self.client.force_authenticate(user=user)

        url = reverse('user-list')
        # url = 'http://127.0.0.1:8000/account/users/'
        # response = self.client.post(url, data, format='json')
        response = self.client.get(url)
        # response = self.client.get(url, urlheaders={'Authorization': 'token ' + response.data['token']})
        # self.client.credentials(Authorization='Token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_4_get_me(self):
        """
        Ensure we can retrieve all users.
        """

        # token = Token.objects.get(user__username='lauren')
        # client = APIClient()
        # client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.__user_login('admin', 't12345')
        print(f"\n{response.data['token']}")
        authorization = 'token ' + response.data['token']
        print(authorization)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + response.data['token'])
        # self.client.credentials(Authorization=authorization)

        # user = User.objects.get(username='admin')
        # self.client.force_authenticate(user=user)

        # url = reverse('me')
        url = 'http://127.0.0.1:8000/account/users/'
        # response = self.client.post(url, data, format='json')
        print(url)
        response = self.client.get(url)
        # response = self.client.get(url, urlheaders={'Authorization': 'token ' + response.data['token']})
        # self.client.credentials(Authorization='token bf8b1e22c00bc3b3f780573392b9ec577fc3057c')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
