from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('feed', views.feed, name='feed'),
    path('addpost', views.addpost, name='addpost'),
    path('profile/<str:displayname>', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('logout',views.logout,name='logout'),
    path('bookmarks', views.bookmarks, name='bookmarks'),
    path('testfunction', views.testfunction, name='testfunction'),
    path('createpost', views.createpost, name='createpost'),
    path('search_song', views.search_song, name='search_song'),
    path('follow', views.follow, name='follow'),
    path('unfollow', views.unfollow, name='unfollow'),
    path('bookmarks', views.bookmarks, name='bookmarks'),
    path('bookmark', views.bookmark, name='bookmark'),
    path('unbookmark', views.unbookmark, name='unbookmark'),

    path('like', views.like, name='like'),
    path('unlike', views.unlike, name='unlike'),
    
]