from . import views
from django.urls import path
from django.conf.urls import url
urlpatterns = [
	path('', views.PostList.as_view(), name='home'),
	path('virtual-tour/<slug:slug>', views.VirtualTour, name='VirtualTour'),
    path('p/<slug:slug>/', views.PostDetails, name='post'),
]