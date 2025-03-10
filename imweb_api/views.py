import base64
import random
import time
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import pandas as pd
import numpy as np

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
  
# 예시
def get_imweb_reviews(access_token, max_reviews=1458944):
  """Fetches and updates Imweb reviews with throttling and pagination.

  Args:
    access_token (str): The Imweb API access token.
    max_reviews (int, optional): The maximum number of reviews to process. Defaults to 1000000.

  Returns:
    None
  """

  api_url = "https://api.imweb.me/v2/shop/reviews&rating=3&limit=2"
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
    time.sleep(1)  # Adjust sleep duration as needed (minimum 0.2 seconds)

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

      time.sleep(0.4)  # Minimum delay between update requests

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

def get_imweb_products(access_token):
  """Fetches and updates Imweb reviews with throttling and pagination.

  Args:
    access_token (str): The Imweb API access token.
    max_reviews (int, optional): The maximum number of reviews to process. Defaults to 1000000.

  Returns:
    None
  """

  cate_api_url = f"https://api.imweb.me/v2/shop/categories"
  headers = {
      "Content-Type": "application/json",
      "access-token": f"{access_token}",
  }
  cate_api = requests.get(cate_api_url, headers=headers)
  cate_get=json.loads(cate_api.content.decode('utf-8'))
  print(f"cate : {cate_get['data'][0]['code']}")
  cate_num = cate_get['data'][0]['code']

  api_url = "https://api.imweb.me/v2/shop/products"
  headers = {
      "Content-Type": "application/json",
      "access-token": f"{access_token}",
  }
  params = {"version": "latest"}
  # response = requests.get(api_url, headers=headers)
  # print(json.loads(response.content.decode('utf-8')))
  excels = pd.read_excel(r'C:\Users\mosad\Desktop\github\ai_inventory_management\data\data.xlsx')
  print(excels['카테고리ID'][2])
  
  # 
  for i in range(2,len(excels)):
    option_values = excels['필수 옵션값'][i]
    option_values = option_values.split(',')

    option_price = str(excels['필수 옵션가'][i])
    # option_price = '31000,31000,31000,31000,31000,34400,34400,34400,34400,34400,41400,41400,41400,41400'
    option_price = option_price.split(',')

    values_data = []
    values_price = []

    for j in range(len(option_values)):
      values_data.append(option_values[j])
      values_price.append(option_price[j])

    print(values_data)

    new_option = {

        "list": [
            {
                "is_require": True,
                "type": "default",  # 기본 옵션
                "name": excels['필수 옵션명'][i],
                "values": values_data,
            }
        ]

}


    print(new_option)
    product_data ={'categories':cate_num
                   ,'images':excels['대표 이미지 파일명'][i],'name':excels['상품명'][i],
                   'simple_content':'','content':excels['상품 상세정보'][i],'use_mobile_prod_content':'',
                   'mobile_content':'','prod_status':'nosale','subscribe_group_code':'',
                   'subscribe_period':'', 'is_badge_new':'','is_badge_best':'','is_badge_md':'','is_badge_hot':'',
                   'origin':'','maker':'','brand':'','seo_title':'','seo_description':'','seo_access_bot':'',
                   'price':excels['판매가'][i],'price_org': np.round(int(excels['판매가'][i])*1.4,-1),'stock_use':'N',
                   'options':new_option,
        
    }
    response = requests.post(api_url, headers=headers,data=json.dumps(product_data))
    print(json.loads(response.content.decode('utf-8')))
    prd_no = json.loads(response.content.decode('utf-8'))['data']['prod_no']

    op_api_url = f"https://api.imweb.me/v2/shop/products/{prd_no}"
    op_response = requests.get(op_api_url, headers=headers)
    op_no = json.loads(op_response.content.decode('utf-8'))['data']['no']
    time.sleep(0.4)

    op_detail_api_url = f"https://api.imweb.me/v2/shop/products/{prd_no}/options-details"
    op_detail_data = {"rating": 5} 
    op_detail = requests.get(op_detail_api_url, headers=headers)
    print(json.loads(op_detail.content)['data']['list'])
    op_details = json.loads(op_detail.content)['data']['list']
    time.sleep(0.4)
    for k in range(len(op_details)):
      op_details_api = f"https://api.imweb.me/v2/shop/products/{prd_no}/options-details/{k+1}"
      details_data = {'price':values_price[k],'status':'SALE'}
      requests.patch(op_details_api, headers=headers, json=details_data)
      time.sleep(0.4)

    


    if response.status_code == 200:
      print("상품업로드 완료!")
      time.sleep(0.4)
    else:
        print("POST 요청 실패:", response.status_code)
  return 'data'


def edit_imweb_products(access_token):
  """Fetches and updates Imweb reviews with throttling and pagination.

  Args:
    access_token (str): The Imweb API access token.
    max_reviews (int, optional): The maximum number of reviews to process. Defaults to 1000000.

  Returns:
    None
  """

  cate_api_url = f"https://api.imweb.me/v2/shop/categories"
  headers = {
      "Content-Type": "application/json",
      "access-token": f"{access_token}",
  }
  # cate_api = requests.get(cate_api_url, headers=headers)
  # cate_get=json.loads(cate_api.content.decode('utf-8'))
  # print(f"cate : {cate_get['data'][0]['code']}")
  # cate_num = cate_get['data'][0]['code']

  api_url = "https://api.imweb.me/v2/shop/products"
  headers = {
      "Content-Type": "application/json",
      "access-token": f"{access_token}",
  }
  params = {"version": "latest"}
  # response = requests.get(api_url, headers=headers)
  # print(json.loads(response.content.decode('utf-8')))
  excels = pd.read_excel(r'C:\Users\mosad\Desktop\github\ai_inventory_management\data\data.xlsx')
  print(excels['상품번호'][0])
  for i in range(len(excels)):
    prd_num = excels['상품번호'][i]
    print(prd_num)
    details_data = {'name':"[인기상품] "+excels['상품명'][i]}
    requests.patch(api_url+f'/{prd_num}', headers=headers, json=details_data)
    time.sleep(0.26)
  


  
  

  # print(f"Total reviews processed: {total_processed}")


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

    
    return Response('data')


@api_view(['POST'])
def getImwebProducts(request):
    id = request.data.get('id')
    access_token = request.data.get('access_token')
    print('getImwebReviews')
    print(access_token)

    data = get_imweb_products(access_token)
    # print(data)
    print('data')

    
    return Response('data')

@api_view(['POST'])
def editImwebProducts(request):
    id = request.data.get('id')
    access_token = request.data.get('access_token')
    print('getImwebReviews')
    print(access_token)

    data = edit_imweb_products(access_token)
    # print(data)
    print('data')

    
    return Response('data')