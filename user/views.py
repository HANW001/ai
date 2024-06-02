from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import cafe24UserSerializer, imwebUserSerializer
from .models import Cafe24User ,ImwebUser

from django.utils.crypto import get_random_string

@api_view(['GET'])
def getUser(request):
    queryset = Cafe24User.objects.all()
    serializer = cafe24UserSerializer(queryset,many=True)
    return Response(serializer.data)

@api_view(['POST']) 
def createCafe24User(request):
    serializer = cafe24UserSerializer(data=request.data) 
    if serializer.is_valid(): 
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST']) 
def createImwebUser(request):
    serializer = imwebUserSerializer(data=request.data) 
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
        user = Cafe24User.objects.filter(id=id,password=password).first()
        print(user)

        if user is None:
            id = request.data.get('id')
            password = request.data.get('password')
            print(id)
            print(password)
            

            # Try to find the user - You might need to refine this query.
            user = ImwebUser.objects.filter(id=id,password=password).first()
            print(user)

            # Authenticate if the user exists
            if user is not None:
                token = get_random_string(length=32)
                queryset = ImwebUser.objects.filter(id=id)
                serializer = imwebUserSerializer(queryset,many=True)
                return Response({ 'message': 'Login successful','token':token,'userData':serializer.data ,'loginSite':'imweb'}, status=status.HTTP_200_OK)
            else:
                return Response({ 'error': 'Invalid credentials' }, status=status.HTTP_401_UNAUTHORIZED)
            

        # Authenticate if the user exists
        if user is not None:
            token = get_random_string(length=32)
            queryset = Cafe24User.objects.filter(id=id)
            serializer = cafe24UserSerializer(queryset,many=True)
            return Response({ 'message': 'Login successful','token':token,'userData':serializer.data,'loginSite':'cafe24' }, status=status.HTTP_200_OK)
        else:
            return Response({ 'error': 'Invalid credentials' }, status=status.HTTP_401_UNAUTHORIZED)

        
    