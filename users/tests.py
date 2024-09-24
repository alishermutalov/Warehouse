from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User  

class UserAPITests(APITestCase):

    def test_create_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  

    def test_update_user_info(self):
        url = reverse('update') 
        self.client.login(username='testuser', password='testpassword123')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_change_password(self):
        url = reverse('change-password')  
        self.client.login(username='testuser', password='testpassword123')
        data = {
            'old_password': 'testpassword123',
            'new_password': 'newpassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_login(self):
        url = reverse('login') 
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_username_validation(self):
        url = reverse('register') 
        data = {
            'username': '',  
            'password': 'testpassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
