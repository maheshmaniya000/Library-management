# Library Management System - Test Guide

## Running Tests

### Run all tests
```bash
python manage.py test
```

### Run specific app tests
```bash
# User app tests only
python manage.py test user

# Books app tests only
python manage.py test books
```

### Run specific test class
```bash
python manage.py test user.tests.UserRegistrationTests
python manage.py test books.tests.BookBorrowTests
```

### Run with verbosity
```bash
python manage.py test --verbosity=2
```

### Run with coverage (install coverage first: pip install coverage)
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## Test Coverage

### User App Tests (`user/tests.py`)

#### UserRegistrationTests
- ✓ Successful user registration with JWT tokens
- ✓ Password mismatch validation
- ✓ Duplicate email validation
- ✓ Missing required fields validation

#### UserLoginTests
- ✓ Successful login with JWT tokens
- ✓ Invalid credentials handling
- ✓ Non-existent user handling
- ✓ Missing fields validation

#### UserProfileTests
- ✓ Get profile when authenticated
- ✓ Unauthorized access when not authenticated

#### UsersListTests
- ✓ Get list of users (excluding superusers)

### Books App Tests (`books/tests.py`)

#### BookListTests
- ✓ Public access to books list
- ✓ Public access to book details

#### BookCreateTests
- ✓ Create book as superuser
- ✓ Prevent creation by regular users
- ✓ Prevent creation by unauthenticated users

#### BookUpdateDeleteTests
- ✓ Update book as superuser
- ✓ Prevent update by regular users
- ✓ Delete book as superuser
- ✓ Prevent deletion by regular users

#### BookBorrowTests
- ✓ Borrow available book when authenticated
- ✓ Prevent borrowing unavailable books
- ✓ Prevent borrowing when unauthenticated

#### IntegrationTests
- ✓ Complete user flow: register → login → borrow book
- ✓ Complete admin flow: create → update → delete book

## Test Data

All tests use isolated test databases and are cleaned up automatically after each test.

### Sample Test Users
- Regular user: `testuser` / `TestPass123!`
- Superuser: `admin` / `AdminPass123!`

### Sample Test Books
- Title: "Test Book 1", ISBN: "1234567890"
- Title: "Test Book 2", ISBN: "0987654321"

## Expected Test Results

All tests should pass. If any test fails, check:
1. Database configuration in `.env`
2. All migrations are applied
3. Required dependencies are installed
4. JWT settings are properly configured
