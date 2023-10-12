from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='common'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
]
