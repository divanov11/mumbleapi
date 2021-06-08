from django.urls import path
from . import views

app_name = 'mumbles-api-discussions'


urlpatterns = [
    path('',views.discussions,name='discussions'),
    path('create/',views.create_discussion,name='create-discussion'),
    path('vote/',views.update_vote,name='discussion-vote'),
    path('<str:pk>/', views.get_discussion, name="get-discussion"),
    path('edit/<str:pk>/', views.edit_discussion, name="edit-discussion"),
    path('delete/<str:pk>/', views.delete_discussion, name="delete-discussion"),
    path('edit-comment/<str:pk>/', views.edit_discussion_comment, name="edit-discussion-comment"),
    path('delete-comment/<str:pk>/', views.delete_discussion_comment, name="delete-discussion-comment"),
]
