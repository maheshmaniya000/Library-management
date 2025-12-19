from django.contrib import admin
from .models import Book, Loan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin interface for Book model"""
    list_display = ['title', 'author', 'isbn', 'page_count', 'availability', 'created']
    list_filter = ['availability', 'created']
    search_fields = ['title', 'author', 'isbn']
    ordering = ['-created']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Admin interface for Loan model"""
    list_display = ['book', 'user', 'loan_date', 'return_date', 'created']
    list_filter = ['loan_date', 'return_date']
    search_fields = ['book__title', 'user__username']
    ordering = ['-loan_date']
    