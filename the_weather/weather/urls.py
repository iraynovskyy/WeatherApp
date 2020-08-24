from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('detail/<city_name>/', views.detail_city, name='detail_city'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('detail/<city_name>/logout/', views.logout_detail, name='logout_detail'),
]