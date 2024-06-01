from django.contrib import admin
from django.urls import include, path

from user.views import createCafe24User, createImwebUser,getUser, loginUser

urlpatterns = [

    path('getUser/', getUser),
    path('postCafe24User/', createCafe24User),
    path('postImwebUser/', createImwebUser),
    path('login/', loginUser),

]