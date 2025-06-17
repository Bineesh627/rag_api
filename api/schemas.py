from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import serializers

class QueryResponseSerializer(serializers.Serializer):
    query = serializers.CharField()
    response = serializers.CharField()
    sources = serializers.ListField(child=serializers.DictField())

QUERY_SCHEMA = extend_schema(
    responses={
        200: OpenApiResponse(response=QueryResponseSerializer),
        400: OpenApiResponse(description="Invalid input"),
        500: OpenApiResponse(description="Server error")
    }
)