from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/read/',views.readNotification,name='read-notification'),
    path('<str:pk>/', views.getNotification, name="get-notification"),
]
