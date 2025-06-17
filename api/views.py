from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuerySerializer
from rag_engine.chain import RAGChain
from chat_history.models import ChatHistory
import logging
import time

logger = logging.getLogger(__name__)

class QueryView(APIView):
    # Add this to disable CSRF for this view (use with caution)
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        start_time = time.time()
        serializer = QuerySerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        query_list = serializer.validated_data['query']
        query = " ".join(query_list)
        session_id = serializer.validated_data.get('session_id', 'global-session')
        
        try:
            rag = RAGChain()
            response, sources = rag.generate(query)
            
            ChatHistory.objects.create(
                session_id=session_id,
                query=query,
                response=response,
                metadata={'sources': sources}
            )
            
            return Response({
                'query': [query],
                'response': [response],
                'sources': sources
            })
        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            elapsed = (time.time() - start_time) * 1000
            logger.info(f"Request processed in {elapsed:.2f}ms")