from django.contrib import admin
from django.urls import include, path

from imweb_api.views import getImweb,getImwebReviews,getImwebProducts,editImwebProducts

urlpatterns = [

    path('getImweb/', getImweb),
    path('getImwebReviews/', getImwebReviews),
    path('getProducts/',getImwebProducts),
    path('editProducts/',editImwebProducts)

]