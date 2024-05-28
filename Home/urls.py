from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('sub/<slug:slug>',views.subscribe,name='sub'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('toggle_meal_off/', views.meal_off_view, name='toggle_meal_off'),
   
]
