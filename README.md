# 재고관리 예측모델 개발

| 이름   | 언어   |
| ------ | ------ |
| 김한울 | 파이썬 |

- 프레임워크 다운

```
pip install -r requirements.txt
```

- 가상환경

```
python -m venv venv
```

- 가상환경 실행

```
.\venv\Scripts\activate
```

- 장고 폴더생성

```python
django-admin startproject ai_Django .
```

- 서버실행

```python
python manage.py runserver
```

- setting.py

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    "order",
    "user",
]

ALLOWED_HOSTS = ['*']

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': name,# 설정값
        'USER' : id,# 설정값
        'PASSWORD' :  pwd,# 설정값
        'HOST' : '127.0.0.1', # 설정값
        'PORT' : '3306',
    }
}

```

- user
  - 회원가입 (Join 버튼)
  - 로그인
- order
  - 카페24 oauth
  - 해당 아이디 주문 가져오기(지금은 2021-01-01부터)
