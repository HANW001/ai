from rest_framework import serializers
from .models import Order

# serializer.py
class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = '__all__'