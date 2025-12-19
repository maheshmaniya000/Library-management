from django.db import models
from user.models import User , Base

# Book model containing fields such as title, author, ISBN, page count, availability, etc.
# Loan model to track which user borrowed which book and when.

class Book(Base):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=255)
    page_count = models.IntegerField()
    availability = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Loan(Base):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.book.title