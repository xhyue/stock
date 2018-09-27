from django.conf.urls import url
from deal import views

urlpatterns = [
    url(r'^deal/',views.deal,name= "deal"),

]
