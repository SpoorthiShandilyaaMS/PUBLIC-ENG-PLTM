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
from django.conf.urls.static import static
from django.conf  import settings


urlpatterns = [
    path('admin', admin.site.urls),
    path('home',views.home_view,name='homeview'),
    path('aboutus',views.aboutus_view,name='aboutus'),
    path('contact',views.contact_view,name='contact'),
    path('signup',views.get_signup_data,name='signup'),
    path('login',views.login,name='login'),
    path('addFeed',views.add_feed,name='addfeed'),
    path('manageFeed',views.manageFeed,name='manageFeed'),
    path('getAllFeeds',views.get_all_feeds,name='getAllFeeds'),
    path('editfeed',views.edit_feed,name='editfeeds'),
    path('deleteFeed',views.delete_feed,name='deleteFeed'),
    path('addcomplaint',views.add_complaint,name='addcomplaint'),
    path('getallcomplaints',views.get_all_complaints,name='getallcomplaints'),
    path('complaint',views.get_all_complaints,name='complaint'),
    path('repcomplaint',views.repcomplaints,name='complaint'),
    path('addquery',views.add_query,name='addquery'),
    path('getallqueries',views.get_all_queries,name='getallqueries'),
    path('deletequery',views.delete_query,name='deletequery'),
    path('editquery',views.edit_query,name='editquery'),
    path('upvote',views.upvote,name='upvote'),
    path('addanswer',views.add_answer,name='addanswer'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('feedback',views.feedback,name='feedback'),
    path('getallfeedback',views.get_all_feedbacks,name='getallfeedback'),
    path('talk',views.talk,name='talk'),
    path('getallqna',views.getqna,name='getqna'),
    path('getassembly',views.getassembly,name='getassembly'),
    path('assembly',views.assembly,name='assembly'),
    path('rti',views.getrti,name='rti'),

   

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
