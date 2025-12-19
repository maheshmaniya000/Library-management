from rest_framework.response import Response
from rest_framework import status

def wrap_response(success, code, data=None, errors=None, status_code=None,message=None):
    response_data = {
        "success": success,
        "code": code
    }
    if not status_code:
        status_code = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
    if errors:
        response_data["errors"] = errors
    if data != None:
        response_data["data"] = data
    if message:
        response_data["message"] = message
    return Response(response_data, status=status_code)
