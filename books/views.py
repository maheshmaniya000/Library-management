from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from library_app.utils import wrap_response
from rest_framework.permissions import IsAuthenticated , AllowAny
from library_app.permissions import IsSuperUser
from .models import Book , Loan
from .serializers import BookSerializer, BookCreateUpdateSerializer, LoanSerializer
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size' 
    max_page_size = 20 

class BookAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated(),IsSuperUser()]


    def get(self , request):
        books = Book.objects.all()
        paginator = BookPagination()
        result_page = paginator.paginate_queryset(books,request)
        serializer = BookSerializer(result_page , many=True)
        return wrap_response(
            success=True,
            code="books_retrieved",
            data={
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "books": serializer.data,
            } , 
            status_code=status.HTTP_200_OK)
    
    def post(self , request):
        serializer = BookCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return wrap_response(success=True , code="book_created" , message='Book created successfully' , data=serializer.data , status_code=status.HTTP_201_CREATED)
        return wrap_response(success=False , code="book_creation_failed" , message='Book creation failed' , data=serializer.errors , status_code=status.HTTP_400_BAD_REQUEST)

    def patch(self , request , pk):
        book = Book.objects.get(pk=pk)
        serializer = BookCreateUpdateSerializer(book , data=request.data , partial=True)    
        if serializer.is_valid():
            serializer.save()
            return wrap_response(success=True , code="book_updated" , message='Book updated successfully' , data=serializer.data , status_code=status.HTTP_200_OK)
        return wrap_response(success=False , code="book_update_failed" , message='Book update failed' , data=serializer.errors , status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , pk):
        book = Book.objects.get(pk=pk)
        book.delete()
        return wrap_response(success=True , code="book_deleted" , message='Book deleted successfully' , status_code=status.HTTP_200_OK)

class BorrowBookAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(),IsSuperUser()]
        else:
            return [IsAuthenticated()]
    
    def post(self , request):
        book_id = request.data.get('book_id')
        if not book_id:
            return wrap_response(success=False , code="book_id_required" , message='Book id is required' , status_code=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(pk=book_id,availability=True)
        except Book.DoesNotExist:
            return wrap_response(success=False , code="book_not_available" , message='Book not available' , status_code=status.HTTP_400_BAD_REQUEST)
        book.availability = False
        book.save()
        Loan.objects.create(book=book , user=request.user)
        return wrap_response(success=True , code="book_borrowed" , message='Book borrowed successfully' , status_code=status.HTTP_200_OK)

    def get(self , request):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans , many=True)
        return wrap_response(success=True , code="loans_retrieved" , message='Loans retrieved successfully' , data=serializer.data , status_code=status.HTTP_200_OK)


class ReturnBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self , request):
        book_id = request.data.get('book_id')
        if not book_id:
            return wrap_response(success=False , code="book_id_required" , message='Book id is required' , status_code=status.HTTP_400_BAD_REQUEST)
        # Update loan only if not already returned
        updated_loan = (
            Loan.objects
            .filter(
                user=request.user,
                book_id=book_id,
                return_date__isnull=True
            )
            .update(return_date=timezone.now())
        )

        if updated_loan == 0:
            return wrap_response(
                success=False,
                code="book_not_found",
                message="book not found or already returned",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Update book availability only if currently unavailable
        Book.objects.filter(
            id=book_id,
            availability=False
        ).update(availability=True)

        return wrap_response(
            success=True,
            code="book_returned",
            message="Book returned successfully",
            status_code=status.HTTP_200_OK
        )