from django.contrib import admin
from django.urls import include, path

from orders.views import OrderViewSet

urlpatterns = [

    path('orderview/',OrderViewSet),

]