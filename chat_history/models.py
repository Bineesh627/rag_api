from django.db import models
from django.utils import timezone

class ChatHistory(models.Model):
    session_id = models.CharField(max_length=255, db_index=True)
    query = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Chat Histories'

    def __str__(self):
        return f"{self.session_id} - {self.created_at}"