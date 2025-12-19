from django.urls import path
from .views import BookAPIView, BorrowBookAPIView , ReturnBookAPIView, BookSearchAPIView

urlpatterns = [
    path('', BookAPIView.as_view(), name='books'),
    path('<int:pk>/', BookAPIView.as_view(), name='books'),
    path('borrow/', BorrowBookAPIView.as_view(), name='borrow_book'),
    path('return/', ReturnBookAPIView.as_view(), name='return_book'),
    path('search/', BookSearchAPIView.as_view(), name='search_book'),
    
]
