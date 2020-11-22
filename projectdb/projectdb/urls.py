"""projectdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from appdb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name='homeview'),
    path('signup',views.get_signup_data,name='signup'),
    path('login',views.login,name='login'),
    path('addFeed',views.add_feed,name='addfeed'),
    path('manageFeed',views.manageFeed,name='manageFeed'),
    path('getAllFeeds',views.get_all_feeds,name='getAllFeeds'),
    path('editfeed',views.edit_feed,name='editfeeds'),
    path('deleteFeed',views.delete_feed,name='deleteFeed'),
    path('addcomplaint',views.add_complaint,name='addcomplaint'),
    path('getallcomplaints',views.get_all_complaints,name='getallcomplaints'),
    path('addquery',views.add_query,name='addquery'),
    path('getallqueries',views.get_all_queries,name='getallqueries'),
    path('upvote',views.upvote,name='upvote'),
    path('addanswer',views.add_answer,name='addanswer'),
    path('dashboard',views.dashboard,name='dashboard')

]
