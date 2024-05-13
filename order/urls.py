from django.contrib import admin
from django.urls import include, path

from order.views import getAccess, getOauth, getOrder
urlpatterns = [

    
    path('getOauth/', getOauth),
    path('getAccess/', getAccess),
    path('getOrder/', getOrder),
    # path('login/', loginUser),

]