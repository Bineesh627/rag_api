import logging
from datetime import datetime, timedelta
from .models import ChatHistory
from django.db.models import Q

logger = logging.getLogger(__name__)

def log_chat_entry(session_id, query, response, metadata=None):
    """
    Creates a new chat history entry in the database
    """
    try:
        return ChatHistory.objects.create(
            session_id=session_id,
            query=query,
            response=response,
            metadata=metadata or {}
        )
    except Exception as e:
        logger.error(f"Failed to log chat entry: {str(e)}")
        return None

def get_session_history(session_id, limit=20, hours=None):
    """
    Retrieves chat history for a specific session
    Optionally filters by time window (last N hours)
    """
    try:
        queryset = ChatHistory.objects.filter(session_id=session_id)
        
        if hours:
            time_threshold = datetime.now() - timedelta(hours=hours)
            queryset = queryset.filter(created_at__gte=time_threshold)
            
        return queryset.order_by('-created_at')[:limit]
    except Exception as e:
        logger.error(f"Failed to retrieve session history: {str(e)}")
        return ChatHistory.objects.none()

def summarize_session(session_id):
    """
    Generates a summary of a chat session
    (Placeholder for future implementation with LLM)
    """
    history = get_session_history(session_id)
    if not history:
        return "No conversation history found"
    
    # This would be replaced with actual LLM summarization in production
    return f"Session contains {len(history)} messages about various topics."

def clear_old_history(days=30):
    """
    Deletes chat history older than specified days
    Returns count of deleted items
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        old_history = ChatHistory.objects.filter(created_at__lt=cutoff_date)
        count = old_history.count()
        old_history.delete()
        logger.info(f"Cleared {count} old chat history records")
        return count
    except Exception as e:
        logger.error(f"Failed to clear old history: {str(e)}")
        return 0

def search_chat_history(query, session_id=None):
    """
    Searches through chat history content
    """
    try:
        search_query = Q(query__icontains=query) | Q(response__icontains=query)
        if session_id:
            search_query &= Q(session_id=session_id)
        return ChatHistory.objects.filter(search_query).order_by('-created_at')
    except Exception as e:
        logger.error(f"Chat history search failed: {str(e)}")
        return ChatHistory.objects.none()