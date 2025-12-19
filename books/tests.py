from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from books.models import Book, Loan


class BookListTests(TestCase):
    """Test cases for book list API"""
    
    def setUp(self):
        self.client = APIClient()
        self.books_url = reverse('books')
        
        # Create author user
        self.author_user = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='Pass123!',
            first_name='Author',
            last_name='User'
        )
        
        # Create test books
        Book.objects.create(
            title='Test Book 1',
            author=self.author_user,
            isbn='1234567890',
            page_count=200,
            availability=True
        )
        Book.objects.create(
            title='Test Book 2',
            author=self.author_user,
            isbn='0987654321',
            page_count=300,
            availability=False
        )
    
    def test_get_books_list_public(self):
        """Test getting books list without authentication"""
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])


class BookCreateTests(TestCase):
    """Test cases for book creation API"""
    
    def setUp(self):
        self.client = APIClient()
        self.books_url = reverse('books')
        
        # Create regular user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Pass123!',
            first_name='Test',
            last_name='User'
        )
        
        # Create superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User'
        )
        
        self.valid_book_data = {
            'title': 'New Book',
            'author': self.superuser.id,  # Author is the user who added the book
            'isbn': '1111111111',
            'page_count': 250,
            'availability': True
        }
    
    def test_create_book_as_superuser(self):
        """Test creating book as superuser"""
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.books_url, self.valid_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'New Book')
    
    def test_create_book_as_regular_user(self):
        """Test creating book as regular user (should fail)"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.books_url, self.valid_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_create_book_unauthenticated(self):
        """Test creating book without authentication (should fail)"""
        response = self.client.post(self.books_url, self.valid_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 0)


class BookUpdateDeleteTests(TestCase):
    """Test cases for book update and delete APIs"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create superuser first
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User'
        )
        
        # Create test book with superuser as author
        self.book = Book.objects.create(
            title='Original Title',
            author=self.superuser,
            isbn='1234567890',
            page_count=200,
            availability=True
        )
        
        # Create regular user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Pass123!',
            first_name='Test',
            last_name='User'
        )
    
    def test_update_book_as_regular_user(self):
        """Test updating book as regular user (should fail)"""
        self.client.force_authenticate(user=self.user)
        url = reverse('books', kwargs={'pk': self.book.id})
        data = {'title': 'Updated Title'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_as_superuser(self):
        """Test deleting book as superuser"""
        self.client.force_authenticate(user=self.superuser)
        url = reverse('books', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(Book.objects.count(), 0)
    
    def test_delete_book_as_regular_user(self):
        """Test deleting book as regular user (should fail)"""
        self.client.force_authenticate(user=self.user)
        url = reverse('books', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 1)


class BookBorrowTests(TestCase):
    """Test cases for book borrowing API"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Pass123!',
            first_name='Test',
            last_name='User'
        )
        
        # Create test book with user as author
        self.book = Book.objects.create(
            title='Borrowable Book',
            author=self.user,
            isbn='1234567890',
            page_count=200,
            availability=True
        )
    
    def test_borrow_book_authenticated(self):
        """Test borrowing book when authenticated"""
        self.client.force_authenticate(user=self.user)
        url = reverse('borrow_book')
        response = self.client.post(url, {'book_id': self.book.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        # Check book availability updated
        self.book.refresh_from_db()
        self.assertFalse(self.book.availability)
        
        # Check loan created
        self.assertEqual(Loan.objects.count(), 1)
        loan = Loan.objects.first()
        self.assertEqual(loan.user, self.user)
        self.assertEqual(loan.book, self.book)

    
    def test_borrow_book_unauthenticated(self):
        """Test borrowing book without authentication"""
        book = Book.objects.first()
        url = reverse('borrow_book')
        response = self.client.post(url,{'book_id': book.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class IntegrationTests(TestCase):
#     """Integration tests for complete user flows"""
    
#     def setUp(self):
#         self.client = APIClient()
    
#     def test_complete_user_registration_and_book_borrowing_flow(self):
#         """Test complete flow: register -> login -> borrow book"""
        
#         # Step 1: Register user
#         register_data = {
#             'username': 'newuser',
#             'email': 'newuser@example.com',
#             'password': 'NewPass123!',
#             'password2': 'NewPass123!',
#             'first_name': 'New',
#             'last_name': 'User',
#             'role': 'user'
#         }
#         register_response = self.client.post(reverse('register'), register_data, format='json')
#         self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
#         access_token = register_response.data['data']['access']
        
#         # Step 2: Create a book (as superuser)
#         superuser = User.objects.create_superuser(
#             username='admin',
#             email='admin@example.com',
#             password='AdminPass123!',
#             first_name='Admin',
#             last_name='User'
#         )
#         self.client.force_authenticate(user=superuser)
#         book_data = {
#             'title': 'Integration Test Book',
#             'author': 'Test Author',
#             'isbn': '9999999999',
#             'page_count': 300,
#             'availability': True
#         }
#         book_response = self.client.post(reverse('books'), book_data, format='json')
#         self.assertEqual(book_response.status_code, status.HTTP_201_CREATED)
#         book_id = book_response.data['data']['id']
        
#         # Step 3: Login as regular user
#         login_data = {'username': 'newuser', 'password': 'NewPass123!'}
#         login_response = self.client.post(reverse('login'), login_data, format='json')
#         self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
#         # Step 4: Borrow the book
#         user = User.objects.get(username='newuser')
#         self.client.force_authenticate(user=user)
#         borrow_url = reverse('borrow_book', kwargs={'pk': book_id})
#         borrow_response = self.client.post(borrow_url)
#         self.assertEqual(borrow_response.status_code, status.HTTP_200_OK)
        
#         # Verify loan created
#         self.assertEqual(Loan.objects.count(), 1)
#         loan = Loan.objects.first()
#         self.assertEqual(loan.user.username, 'newuser')
#         self.assertEqual(loan.book.title, 'Integration Test Book')
        
#         # Verify book is no longer available
#         book = Book.objects.get(id=book_id)
#         self.assertFalse(book.availability)
    
#     def test_admin_book_management_flow(self):
#         """Test complete admin flow: create -> update -> delete book"""
        
#         # Create superuser
#         superuser = User.objects.create_superuser(
#             username='admin',
#             email='admin@example.com',
#             password='AdminPass123!',
#             first_name='Admin',
#             last_name='User'
#         )
#         self.client.force_authenticate(user=superuser)
        
#         # Create book
#         book_data = {
#             'title': 'Admin Test Book',
#             'author': 'Admin Author',
#             'isbn': '1111111111',
#             'page_count': 400,
#             'availability': True
#         }
#         create_response = self.client.post(reverse('books'), book_data, format='json')
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         book_id = create_response.data['data']['id']
        
#         # Update book
#         update_url = reverse('books', kwargs={'pk': book_id})
#         update_data = {
#             'title': 'Updated Admin Book',
#             'author': 'Admin Author',
#             'isbn': '1111111111',
#             'page_count': 450
#         }
#         update_response = self.client.put(update_url, update_data, format='json')
#         self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
#         # Verify update
#         book = Book.objects.get(id=book_id)
#         self.assertEqual(book.title, 'Updated Admin Book')
#         self.assertEqual(book.page_count, 450)
        
#         # Delete book
#         delete_response = self.client.delete(update_url)
#         self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Book.objects.count(), 0)
