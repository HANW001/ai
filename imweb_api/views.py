from django.shortcuts import render

# Create your views here.
import requests
import json

def get_auth_token(api_key, secret):
  """
  IMweb API v2 인증 토큰을 얻는 함수입니다.

  Args:
    api_key (str): IMweb API 키
    secret (str): IMweb API 시크릿 키

  Returns:
    str: 인증 토큰
  """

  payload = {
    "key": api_key,
    "secret": secret
  }

  response = requests.post("https://api.imweb.me/v2/auth", data=json.dumps(payload))

  if response.status_code == 200:
    data = json.loads(response.content)
    return data["token"]
  else:
    raise Exception(f"IMweb API 인증 실패: {response.status_code}")

# 예시

api_key = "{API_KEY}"
secret = "{SECRET}"

token = get_auth_token(api_key, secret)
print(token)