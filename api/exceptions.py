from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is None:
        # Handle uncaught exceptions
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Customize 400 responses
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        response.data = {
            'error': 'Validation error',
            'details': response.data
        }
    
    return response