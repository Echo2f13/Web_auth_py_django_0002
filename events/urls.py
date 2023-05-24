from django.urls import path
from . import views

urlpatterns = [
    path('startUp/', views.index, name='Start_up_page'),
    path('signUp/', views.sign_up_page, name='sign_up_page'),
    path('logIn/', views.log_in_page, name='log_in_page'),
]