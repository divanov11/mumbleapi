from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/read/',views.read_notification,name='read-notification'),
    path('', views.get_notifications, name="get-notifications"),
]
