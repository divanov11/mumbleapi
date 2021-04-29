from django.urls import path
from . import views

urlpatterns = [
    path('',views.discussions,name='discussions'),
    path('create/',views.createDiscussion,name='create-discussion'),
    path('vote/',views.updateVote,name='vote'),
    path('<str:pk>/', views.getDiscussion, name="get-discussion"),
    path('edit/<str:pk>/', views.editDiscussion, name="edit-discussion"),
    path('delete/<str:pk>/', views.deleteDiscussion, name="delete-discussion"),
    path('edit-comment/<str:pk>/', views.editDiscussionComment, name="edit-discussion-comment"),
    path('delete-comment/<str:pk>/', views.deleteDiscussionComment, name="delete-discussion-comment"),
]
