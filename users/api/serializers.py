from rest_framework import serializers

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ('email',)
        
    