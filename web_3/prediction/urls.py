from django.urls import path
from . import views

app_name='prediction'

urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.main, name='main'),
    path('predict/', views.predict, name='predict'),
    path('emp/', views.emp, name='emp'),
]
