from django.views.generic import TemplateView
from django.urls import path
from . import views


urlpatterns = [
    
    path('home/',views.home_page,name="home_page"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.user_login,name="user_login"),
    path('logout/',views.user_logout,name="user_logout"),
    path('email_verify/',views.VerifyEmail.as_view(),name="email_verify"),
]








