from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from .serializers import OrderSerializer
# from cafe24_api import Cafe24API
@api_view()
def OrderViewSet(request):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer

    return Response({"message":'hello world!'})
