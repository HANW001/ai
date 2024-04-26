# 재고관리 예측모델 개발

| 이름   | 언어   |
| ------ | ------ |
| 김한울 | 파이썬 |

- 가상환경

```python
python -m venv venv
```

- 가상환경 실행

```
.\venv\Scripts\activate
```

- 장고설치

```
pip install django
```

- 장고 실행

```python
django-admin startproject ai_Django .
```

- 서버실행

```python
python manage.py runserver
```

- 프레임워크 다운

```
pip install djangorestframework markdown
```

- setting.py

```
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
]
```

