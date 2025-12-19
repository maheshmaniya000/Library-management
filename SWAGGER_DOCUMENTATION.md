# Library Management System - API Documentation

## Automatic API Documentation with Swagger

This project uses **drf-yasg** (Django REST Framework - Yet Another Swagger Generator) for automatic API documentation generation.

## Accessing API Documentation

Once the server is running, you can access the API documentation at:

### Swagger UI (Interactive)
```
http://localhost:8000/swagger/
```
- Interactive API documentation
- Test API endpoints directly from the browser
- See request/response schemas
- Try out authentication

### ReDoc (Alternative UI)
```
http://localhost:8000/redoc/
```
- Clean, responsive documentation
- Better for reading and sharing
- Three-panel design

### OpenAPI Schema (JSON/YAML)
```
http://localhost:8000/swagger.json
http://localhost:8000/swagger.yaml
```
- Raw OpenAPI 2.0 schema
- Use with API clients like Postman, Insomnia

## Using Swagger UI

### 1. Authentication
To test authenticated endpoints:

1. **Register or Login** to get an access token
   - Use `/users/register/` or `/users/login/` endpoint
   - Copy the `access` token from the response

2. **Authorize** in Swagger UI
   - Click the **"Authorize"** button (top right)
   - Enter: `Bearer <your_access_token>`
   - Click **"Authorize"** then **"Close"**

3. **Test Endpoints**
   - All authenticated requests will now include your token
   - Try borrowing a book or accessing your profile

### 2. Testing Endpoints

Each endpoint shows:
- **HTTP Method** (GET, POST, PUT, DELETE)
- **Parameters** (path, query, body)
- **Request Body Schema** (for POST/PUT)
- **Response Codes** and schemas
- **Try it out** button to test

### 3. Example Workflow

1. **Register a user**:
   - Expand `POST /users/register/`
   - Click "Try it out"
   - Fill in the request body
   - Click "Execute"

2. **Login**:
   - Expand `POST /users/login/`
   - Enter username and password
   - Copy the access token

3. **Authorize**:
   - Click "Authorize" button
   - Paste: `Bearer <token>`

4. **Browse Books**:
   - Expand `GET /api/books/`
   - Click "Try it out" and "Execute"

5. **Borrow a Book**:
   - Expand `POST /api/books/borrow/`
   - Enter book_id
   - Click "Execute"

## Features

### Automatic Schema Generation
- Automatically generates OpenAPI schema from Django REST Framework serializers
- No manual documentation writing needed
- Always up-to-date with code changes

### Interactive Testing
- Test all API endpoints directly from the browser
- See real request/response examples
- Validate request bodies before sending

### Authentication Support
- JWT Bearer token authentication
- Easy token management in UI
- Secure endpoint testing

### Request/Response Examples
- Automatic example generation from serializers
- Shows all possible response codes
- Displays validation errors

## Customization

The API documentation is configured in `library_app/urls.py`:

```python
schema_view = get_schema_view(
    openapi.Info(
        title="Library Management API",
        default_version='v1',
        description="...",
        contact=openapi.Contact(email="contact@library.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
```

### Adding Custom Documentation

You can add custom documentation to views using docstrings:

```python
class BookAPIView(APIView):
    """
    List all books or create a new book.
    
    GET: Returns a list of all books
    POST: Create a new book (superuser only)
    """
    
    def get(self, request):
        """
        Retrieve all books.
        
        Returns a paginated list of books with search functionality.
        """
        pass
```

### Adding Request/Response Examples

Use drf-yasg decorators for detailed documentation:

```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BookAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get list of all books",
        responses={
            200: BookSerializer(many=True),
            400: "Bad Request"
        },
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by title, author, or ISBN",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        pass
```

## Benefits

✅ **Always Up-to-Date**: Documentation auto-generates from code  
✅ **Interactive**: Test endpoints without external tools  
✅ **Standardized**: Uses OpenAPI/Swagger standard  
✅ **Easy Sharing**: Share documentation URL with frontend team  
✅ **Client Generation**: Generate API clients from schema  
✅ **No Manual Work**: No need to maintain separate docs  

## Production Considerations

For production, you may want to:

1. **Restrict Access**:
   ```python
   permission_classes=(permissions.IsAdminUser,)
   ```

2. **Disable in Production**:
   ```python
   if settings.DEBUG:
       urlpatterns += [
           path('swagger/', schema_view.with_ui('swagger')),
       ]
   ```

3. **Add API Versioning**:
   ```python
   default_version='v1'
   ```

## Troubleshooting

### Swagger UI not loading
- Check that `drf-yasg` is in INSTALLED_APPS
- Ensure `rest_framework` is properly configured
- Clear browser cache

### Authentication not working
- Make sure to include "Bearer " prefix
- Check token hasn't expired (1 hour default)
- Use token refresh endpoint if needed

### Endpoints not showing
- Check URL routing is correct
- Ensure views are using DRF classes (APIView, ViewSet)
- Verify serializers are properly defined
