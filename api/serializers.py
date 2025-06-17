from rest_framework import serializers

class QuerySerializer(serializers.Serializer):
    query = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        error_messages={
            'required': 'query field is required',
            'not_a_list': 'query must be an array of strings'
        }
    )
    session_id = serializers.CharField(required=False)

    def to_internal_value(self, data):
        try:
            # Handle different input formats
            if isinstance(data.get('query'), str):
                data['query'] = [data['query']]
            return super().to_internal_value(data)
        except Exception as e:
            raise serializers.ValidationError({
                'error': 'Invalid input format',
                'details': str(e)
            })