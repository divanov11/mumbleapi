from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_messages, name="get-messages"),
    path('<str:pk>/read/', views.read_message, name="read-message"),
    path('unread/count/', views.get_unread_messages_count, name="get-unread-messages-count"),
    path('create/', views.create_message, name="create-message"),
]
