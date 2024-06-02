import base64
import random
import time
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import requests
import json

def get_auth_token(api_key, secret):
  """
  IMweb API v2 인증 토큰을 얻는 함수입니다. (GET 방식)

  Args:
    api_key (str): IMweb API 키
    secret (str): IMweb API 시크릿 키

  Returns:
    str: 인증 토큰
  """
  headers = {
    "Content-Type": "application/json",
  }
  request_data = {
    "key": f"{api_key}",
    "secret": f"{secret}",
  }

  response = requests.get("https://api.imweb.me/v2/auth", headers=headers,json=request_data)

  if response.status_code == 200:
    data = json.loads(response.content)
    return data
  else:
    raise Exception(f"IMweb API 인증 실패: {response.status_code}")
  

# def get_imweb_reviews(access_token):
#     api_url = "https://api.imweb.me/v2/shop/reviews&rating=3"
#     headers = {
#         "Content-Type": "application/json",
#         "access-token": f"{access_token}",
#     }

#     params = {
#         "version": "latest",
#     }

#     response = requests.get(api_url, headers=headers, params=params)
#     if response.status_code == 200:
#       data = json.loads(response.content)
      
#       data_len = data['data']['list']
#       print(len(data_len))
#       for i in range(len(data_len)):
#           if data_len[i]['type'] != 'npay':
             
#             review_id = data_len[i]['idx']
#             review_data = {
#                 "rating": 5,  # Example: Update rating to 5
#             }
#             print(f'{review_id} {review_data}')

#             update_imweb_review_response = update_imweb_review(review_id, access_token, review_data)

#             if update_imweb_review_response.status_code == 200:
#                 print("Review updated successfully!")
#                 # Handle successful response
#             else:
#                 print("Error updating review:", update_imweb_review_response.status_code, update_imweb_review_response.text)
#                 # Handle error response
         
#       return data
#     else:
#       raise Exception(f"IMweb API 인증 실패: {response.status_code}")
    
# def update_imweb_review(review_id, access_token, review_data):
#     time.sleep(0.55)
#     """Updates an Imweb review.

#     Args:
#         review_id (int): The ID of the review to update.
#         access_token (str): The Imweb API access token.
#         review_data (dict): The data to update the review with.

#     Returns:
#         requests.Response: The API response object.
#     """

#     api_url = f"https://api.imweb.me/v2/shop/reviews/{review_id}"
#     headers = {
#         "Content-Type": "application/json",
#         "access-token": f"{access_token}",
#     }

#     response = requests.patch(api_url, headers=headers, json=review_data)
#     print(response)
#     return response
# 예시
def get_imweb_reviews(access_token, max_reviews=907324):
  """Fetches and updates Imweb reviews with throttling and pagination.

  Args:
    access_token (str): The Imweb API access token.
    max_reviews (int, optional): The maximum number of reviews to process. Defaults to 1000000.

  Returns:
    None
  """

  api_url = "https://api.imweb.me/v2/shop/reviews&rating=3"
  headers = {
      "Content-Type": "application/json",
      "access-token": f"{access_token}",
  }
  params = {"version": "latest"}

  offset = 0
  total_processed = 0

  while total_processed < max_reviews:
    data = fetch_review_page(api_url, headers, params, offset)
    if not data:
      break  # No more reviews to fetch

    total_processed += update_reviews(access_token, data)
    offset += len(data['data']['list'])
    # time.sleep(1)  # Adjust sleep duration as needed (minimum 0.2 seconds)

  print(f"Total reviews processed: {total_processed}")

def fetch_review_page(api_url, headers, params, offset):
  """Fetches a page of reviews from the Imweb API.

  Args:
    api_url (str): The Imweb API endpoint URL.
    headers (dict): The request headers.
    params (dict): The request query parameters.
    offset (int): The offset for pagination.

  Returns:
    dict or None: The fetched review data or None if no more reviews.
  """

  params["offset"] = offset
  response = requests.get(api_url, headers=headers, params=params)

  if response.status_code == 200:
    return json.loads(response.content)
  else:
    raise Exception(f"IMweb API error: {response.status_code}")

def update_reviews(access_token, data):
  """Updates reviews in the provided data with throttling.

  Args:
    access_token (str): The Imweb API access token.
    data (dict): The review data containing a list of reviews.

  Returns:
    int: The number of successfully updated reviews.
  """

  updated_count = 0
  for review in data['data']['list']:
    if review['type'] != 'npay':
      review_id = review['idx']
      review_data = {"rating": 5}  # Update rating to 5 (example)
      update_response = update_imweb_review(review_id, access_token, review_data)

      if update_response.status_code == 200:
        print(f"Review {review_id} updated successfully!")
        updated_count += 1
      else:
        print(f"Error updating review {review_id}: {update_response.status_code}")

      time.sleep(0.5)  # Minimum delay between update requests

  return updated_count

def update_imweb_review(review_id, access_token, review_data):
  """Updates an Imweb review.

  Args:
    review_id (int): The ID of the review to update.
    access_token (str): The Imweb API access token.
    review_data (dict): The data to update the review with.

  Returns:
    requests.Response: The API response object.
  """

  api_url = f"https://api.imweb.me/v2/shop/reviews/{review_id}"
  headers = {
      "Content-Type": "application/json",
      "access-token": f"{access_token}",
  }

  return requests.patch(api_url, headers=headers, json=review_data)


@api_view(['POST'])
def getImweb(request):
    id = request.data.get('id')
    api_key = request.data.get('apikey')
    secret = request.data.get('servicekey')
    print(id)

    token_data = get_auth_token(api_key, secret)
    print(token_data)

    
    return Response(token_data)


@api_view(['POST'])
def getImwebReviews(request):
    id = request.data.get('id')
    access_token = request.data.get('access_token')
    print('getImwebReviews')
    print(access_token)

    data = get_imweb_reviews(access_token)
    # print(data)
    print('data')

    
    return Response(data)