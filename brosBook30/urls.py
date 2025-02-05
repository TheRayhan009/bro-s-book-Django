"""
URL configuration for bros_Book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name="home"),
    path('addpost/', views.addpost,name="addpost"),
    path('profile/', views.profile,name="profile"),
    path('userdetailedpost/<slug:link>/', views.userdetailedpost,name="userdetailedpost"),
    path('signin/', views.signin,name="signin"),
    # path('login/', views.login,name="login"),
    path('emailverification/', views.emailverification,name="emailverification"),
    path('logout/', views.logout,name="logout"),
    path('getpostdata/', views.getpostdata,name="getpostdata"),
    path('like/', views.like,name="like"),
    path('removelike/', views.removelike,name="removelike"),
    path('getprofileposts/', views.getprofileposts,name="getprofileposts"),
    path('detailedpost/<slug:link>/', views.detailedpost,name="detailedpost"),
    path('getcomments/', views.getcomments,name="getcomments"),
    path('addcomments/', views.addcomments,name="addcomments"),
    path('dofollow/', views.dofollow,name="dofollow"),
    path('friends/', views.friends,name="friends"),
    path('getuserfollowers/', views.getuserfollowers,name="getuserfollowers"),
    path('getuserfollowerinfo/', views.getuserfollowerinfo,name="getuserfollowerinfo"),
    path('getuserfollow/', views.getuserfollow,name="getuserfollow"),
    path('getuserfollowinfo/', views.getuserfollowinfo,name="getuserfollowinfo"),
    path('getuserfriends/', views.getuserfriends,name="getuserfriends"),
    path('getuserfriendsinfo/', views.getuserfriendsinfo,name="getuserfriendsinfo"),
    path('inbox/', views.inbox,name="inbox"),
    path('message/<slug:link>', views.message,name="message"),
    path("getmessage/", views.getmessage,name="getmessage"),
    path("sendmessage/", views.sendmessage,name="sendmessage"),
    path("uploadVmessage/", views.uploadVmessage,name="uploadVmessage"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
