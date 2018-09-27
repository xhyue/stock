from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'kdata/', views.k_data, name='kdata'),
    url(r'realhead/', views.realHead, name='realhead'),
    url(r'hotinfo/', views.hotInfo, name='hotinfo'),
    url(r'indexrange/', views.indexRang, name='indexrange'),
    url(r'breakup/', views.breakUp, name='breakup'),

]