from django.db import models

class ModelConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    llm_model = models.CharField(max_length=100)
    embedding_model = models.CharField(max_length=100)
    temperature = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"