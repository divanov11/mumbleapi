from django.urls import path
from . import views

urlpatterns = [
    path('',views.artciles,name='articles'),
    path('create/',views.createArtcile,name='create-article'),
    path('vote/',views.updateVote,name='vote'),
]