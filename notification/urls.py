from django.urls import path

from . import views

urlpatterns = [
    path('<str:pk>/read/',views.readNotification,name='read-notification'),
    path('', views.getNotifications, name="get-notifications"),
]
