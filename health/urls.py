from django.urls import path
from . import views
from .views import predict

urlpatterns = [
    path('', views.home, name='home'),
    path('new_search', views.disease_search, name='new_search'),
    path('about', views.about, name='about'),
    path('chat', predict, name='chat'),
    
]