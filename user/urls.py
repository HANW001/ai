from django.contrib import admin
from django.urls import include, path

from user.views import getUser

urlpatterns = [

    path('getUser/', getUser),

]