from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('about-us/', views.about, name='about'),
    path('MostPopular/', views.MostPopular, name='MostPopular'),
    path('our-policy/', views.policy, name='policy'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    url(r'^search/$', views.searchquery, name='searchquery'),
    path('virtual-tour/<slug:slug>', views.VirtualTour, name='VirtualTour'),
    path('p/<slug:slug>/', views.PostDetails, name='post'),
]
