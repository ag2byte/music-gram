from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('feed', views.feed, name='feed'),
    path('addpost', views.addpost, name='addpost'),
    path('signup', views.signup, name='signup'),
    path('bookmarks',views.bookmarks,name = 'bookmarks')
]