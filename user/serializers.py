from rest_framework import serializers
from .models import User

# serializer.py
class userSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('mall','id', 'password', 'client_id', 'client_secretkey', 'servicekey')