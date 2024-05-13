from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import userSerializer
from .models import User
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string

@api_view(['GET'])
def getUser(request):
    queryset = User.objects.all()
    serializer = userSerializer(queryset,many=True)
    return Response(serializer.data)

@api_view(['POST']) 
def createUser(request):
    serializer = userSerializer(data=request.data) 
    if serializer.is_valid(): 
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def loginUser(request):
    # mall = request.data.get('mall')  # Assuming mall is also sent in the request
    id = request.data.get('id')
    password = request.data.get('password')
    print(id)

    # Try to find the user - You might need to refine this query.
    user = User.objects.filter(id=id,password=password).first()
    print(user)

    # Authenticate if the user exists
    if user is not None:
        token = get_random_string(length=32)
        queryset = User.objects.filter(id=id)
        serializer = userSerializer(queryset,many=True)
        return Response({ 'message': 'Login successful','token':token,'userData':serializer.data }, status=status.HTTP_200_OK)
    else:
        return Response({ 'error': 'Invalid credentials' }, status=status.HTTP_401_UNAUTHORIZED)
    