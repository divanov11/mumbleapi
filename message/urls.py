from django.urls import path
from . import views

urlpatterns = [
    # path('<str:pk>/read/',views.read_message,name='read-notification'),
    path('', views.get_messages, name="get-messages"),
    path('create/', views.create_message, name="create-message"),
]
