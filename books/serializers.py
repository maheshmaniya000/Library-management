from rest_framework import serializers
from .models import Book, Loan


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model"""
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'page_count', 'availability', 'created', 'modified']
        read_only_fields = ['id', 'created', 'modified']
    


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating books (admin only)"""
    
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'page_count', 'availability']
    
    


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loan model"""
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Loan
        fields = ['id', 'book_id', 'book_title', 'user_id', 'user_name', 'loan_date', 'return_date']


