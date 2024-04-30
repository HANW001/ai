from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import userSerializer
from .models import User

@api_view(['GET'])
def getUser(request):
    queryset = User.objects.all()
    serializer = userSerializer(queryset,many=True)
    return Response(serializer.data)