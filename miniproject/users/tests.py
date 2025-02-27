# users/tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from users.serializers import CustomUserSerializer

class UserTests(APITestCase): # Renamed class for brevity

    def test_user_registration(self):
        url = reverse('user-register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')

    def test_user_registration_passwords_mismatch(self):
        url = reverse('user-register')
        data = {
            'username': 'testuser',
            'password': 'password123',
            'password2': 'wrongpassword',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('passwords must match', response.data['password'][0].lower())

    def test_get_user_profile_authenticated(self):
        user = CustomUser.objects.create_user(username='profileuser', password='profilepassword')
        self.client.force_authenticate(user=user)
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CustomUserSerializer(user)
        self.assertEqual(response.data, serializer.data)

    def test_get_user_profile_unauthenticated(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_list_admin_user(self):
        admin_user = CustomUser.objects.create_superuser(username='adminuser', password='adminpassword', email='admin@example.com')
        self.client.force_authenticate(user=admin_user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_list_non_admin_user(self):
        non_admin_user = CustomUser.objects.create_user(username='nonadmin', password='nonadminpassword')
        self.client.force_authenticate(user=non_admin_user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_list_unauthenticated(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)