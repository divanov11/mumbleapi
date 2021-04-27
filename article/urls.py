from django.urls import path
from . import views

urlpatterns = [
    path('',views.artciles,name='articles'),
]