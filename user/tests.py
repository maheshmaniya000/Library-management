from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User


class UserRegistrationTests(TestCase):
    """Test cases for user registration API"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'user'
        }
    
    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
    
    def test_register_user_password_mismatch(self):
        """Test registration with mismatched passwords"""
        data = self.valid_user_data.copy()
        data['password2'] = 'DifferentPass123!'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(User.objects.count(), 0)
    
    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email"""
        User.objects.create_user(
            username='existing',
            email='test@example.com',
            password='Pass123!',
            first_name='Existing',
            last_name='User'
        )
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
    
    def test_register_user_missing_fields(self):
        """Test registration with missing required fields"""
        data = {'username': 'testuser', 'password': 'Pass123!'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])


class UserLoginTests(TestCase):
    """Test cases for user login API"""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
    
    def test_login_success(self):
        """Test successful login"""
        data = {'username': 'testuser', 'password': 'TestPass123!'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {'username': 'testuser', 'password': 'WrongPassword'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        data = {'username': 'nonexistent', 'password': 'TestPass123!'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
    
    def test_login_missing_fields(self):
        """Test login with missing fields"""
        data = {'username': 'testuser'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])


class UserProfileTests(TestCase):
    """Test cases for user profile API"""
    
    def setUp(self):
        self.client = APIClient()
        self.profile_url = reverse('user-profile')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
    
    def test_get_profile_authenticated(self):
        """Test getting profile when authenticated"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], 'testuser')
        self.assertEqual(response.data['data']['email'], 'test@example.com')
    
    def test_get_profile_unauthenticated(self):
        """Test getting profile when not authenticated"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UsersListTests(TestCase):
    """Test cases for users list API"""
    
    def setUp(self):
        self.client = APIClient()
        self.users_url = reverse('users')
        # Create regular users
        User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='Pass123!',
            first_name='User',
            last_name='One'
        )
        User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='Pass123!',
            first_name='User',
            last_name='Two'
        )
        # Create superuser
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User'
        )
    
    def test_get_users_list(self):
        """Test getting list of users (excluding superusers)"""
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        # Should return 2 regular users, not the superuser
        self.assertEqual(len(response.data['data']), 2)
