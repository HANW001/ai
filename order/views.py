from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import orderSerializer
from .models import Order
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string
from datetime import datetime
import requests
import base64

@api_view(['POST'])
def getOrder(request):
    # mall = request.data.get('mall')  # Assuming mall is also sent in the request
    id = request.data.get('id')
    # password = request.data.get('password')
    print(id)

    # Try to find the user - You might need to refine this query.
    orders = Order.objects.filter(order_mall=id).first()
    print(orders)

    # Authenticate if the user exists
    if orders is not None:
        queryset = Order.objects.all()
        serializer = orderSerializer(queryset,many=True)
        print(serializer.data)
        return Response({ 'orderData':serializer.data })
    else:
        return Response({ 'error': 'Invalid credentials' }, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def getOauth(request):
    mallid = request.data.get('id')
    client_id = request.data.get('clientId')
    scope = "mall.write_order, mall.read_order"
    redirect_uri = f'https://{mallid}.cafe24.com/'
    url =  f'https://{mallid}.cafe24api.com/api/v2/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'
    print(url)
    return Response({ 'reUrl':url })

@api_view(['POST'])
def getAccess(request):
    try:
        # Extract data with validation
        mallid = request.data.get('id') 
        code = request.data.get('code')
        client_id = request.data.get('clientId') 
        client_secret = request.data.get('clientSecretkey') 
        # ... add validation for required fields

        # Construct request components
        redirect_uri = f'https://{mallid}.cafe24.com/'
        token_url = f"https://{mallid}.cafe24api.com/api/v2/oauth/token"
        payload = f'''grant_type=authorization_code&code={code}&redirect_uri={redirect_uri}'''
        encoded_auth = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
        print(f'print : {encoded_auth}')
        headers = {
            'Authorization': f"Basic {encoded_auth}",
            'Content-Type': "application/x-www-form-urlencoded"
        }
        print(f'print : {headers}')

        # Send request and handle response
        response = requests.post(token_url, data=payload, headers=headers)
        print(response.text)
        

        return JsonResponse(response.json())  # Assuming JSON response

    except requests.exceptions.RequestException as e:
        # Handle network errors 
        print(f"Request error: {e}")
        return {'error': str(e)}  # Return an error response to client

    except Exception as e:
        # Handle other potential exceptions
        print(f"Unexpected error: {e}")
        return {'error': 'Internal server error'} 
    

@api_view(['POST'])
def getOrder(request):
    print('orders')
    today = datetime.today()
    mallid = request.data.get('id') 
    access_token=request.data.get('access_token') 
    start_date =  '2024-03-01'
    end_date = today.date()
    version= today.date()
    url = f"https://{mallid}.cafe24api.com/api/v2/admin/orders?start_date={start_date}&end_date={end_date}"
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': "application/json",
        # 'X-Cafe24-Api-Version': f"{version}"
        }
    response = requests.request("GET", url, headers=headers)
    response_data = response.json()
    print(len(response_data['orders']))
