# Library Management System

A RESTful API for managing library operations including book management, user authentication, and book borrowing/returning functionality.

## Features

- **User Management**
  - User registration and authentication
  - JWT token-based authentication
  - User roles (Librarian/Patron)

- **Book Management**
  - Add/Edit/Delete books
  - View book details
  - Search and filter books
  - Check book availability

- **Loan Management**
  - Borrow books
  - Return books
  - View loan history
  - Track due dates

## Technology Stack

- **Backend**: Django 5.0
- **Database**: Postgrsql
- **Authentication**: JWT (JSON Web Tokens)
- **API**: Django REST Framework
- **Testing**: Django Test Framework

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd library-management
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Running Tests

```bash
python manage.py test user
python manage.py test books
```

## Project Structure

```
library-management/
├── library_app/           # Main project configuration
├── books/                 # Books app
│   ├── models.py         # Book and Loan models
│   ├── serializers.py    # API serializers
│   ├── views.py         # API views
│   ├── urls.py          # URL routing
│   └── tests.py         # Test cases
├── user/                 # User management app
│   ├── models.py        # Custom user model
│   └── ...
├── manage.py            # Django management script
└── requirements.txt     # Project dependencies
```
