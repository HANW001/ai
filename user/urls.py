from django.contrib import admin
from django.urls import include, path

from user.views import createUser, getUser, loginUser

urlpatterns = [

    path('getUser/', getUser),
    path('postUser/', createUser),
    path('login/', loginUser),

]