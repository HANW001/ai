from rest_framework import serializers
from .models import Cafe24User , ImwebUser

# serializer.py
class cafe24UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cafe24User
        fields = '__all__'

class imwebUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImwebUser
        fields = '__all__'