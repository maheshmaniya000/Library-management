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

