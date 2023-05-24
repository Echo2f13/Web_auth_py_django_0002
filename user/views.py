from datetime import datetime, timedelta
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import socket
from django.contrib.sites.shortcuts import get_current_site
from .models import User
import jwt
from rest_framework import views
from rest_framework_simplejwt.tokens import RefreshToken


from web_auth import settings
from user.models import User 
from django.core.mail import send_mail 
from web_auth.settings import EMAIL_HOST_USER 
from django.urls import reverse 

from django.http import HttpResponse 
from django.template import loader
from django.shortcuts import redirect, render


sender_address = 'manishdevrock@gmail.com'
sender_pass = '7207702799'
socket.getaddrinfo('localhost', 8000)

is_active_verify = False #this is for user email activation (verification)



def home_page(request):
  return render(request,'home.html')





def signup(request):
    try:
        if request.user.is_authenticated:
           return redirect('home_page')
        else:
            if request.method == 'POST':
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']
                 
                message1 = 0 #this message will pop up when user already exist
                message2 = 0 # this message will pop up when the user successfully create an account

                if User.objects.filter(username = username).exists():
                    message1 = 1
                    return render(request,'regpage.html',{'message1': message1 })
                else :
                   user = User.objects.create_user(username=username, email=email, password=password, is_active=is_active_verify)
                   user.save();
                   
                   print('data recieced')
                   message2 = 1

                   user_email = User.objects.get(email=email)
                   token = RefreshToken.for_user(user_email).access_token
                   token.set_exp(lifetime=timedelta(days=36500))
                   current_site = get_current_site(request).domain
                   relativeLink = reverse('email_verify')
                   Email = email
                   absUrl = 'http://' + current_site + relativeLink + "?token=" + str(token)
                   Subject = " Hello " + "Your Account creation was Successful"
                   Message = " Mr/Ms " +  "Click below link to verify your account \n " + absUrl
                   send_mail(Subject, Message, EMAIL_HOST_USER, [Email])
                   print('pass1')
                   print(absUrl)
                   return render(request, 'login.html', { 'message2' : message2 })
    except IntegrityError:
        print('pass2')
        return render(request, 'regpage.html', {'message3': 'These is some error please try again'})
    print('pass3')
    return render(request, 'regpage.html', {'error': 'error'})

# def email_verified(request):
    
#     is_active = 1 #active when user invokes this function

class VerifyEmail(views.APIView):
    def get(self, request):
        token = request.GET.get('token')
        print('token=', token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(payload)

            user = User.objects.get(id=payload['user_id'])
            print(user)
            if not user.is_active:
                user.is_active = True
                user.save()

            return render(request, 'email_verify.html')
        except jwt.ExpiredSignatureError as identifier:
            return render(request, 'email_verify.html')


def user_login(request):
   if request.user.is_authenticated:
       return redirect('home_page')
   else:
       error = 0

       if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]
            incorrect_credentials = 0
            user = authenticate(username = username, password = password)
            data = User.objects.filter(username=username).first()
            print(username,password)
            print(user)
            print(data)
            print('001')
            if User.objects.filter(username = username ).exists():
                print('002')
                if  data.is_active == True :
                    is_active_verify = True
                    print('003')
                    login(request, user)
                    print('logged in after 003')
                    return render(request, 'home.html', {'is_active': is_active_verify})
                else :
                    # print('004')
                    # is_active_verify = False
                    # login(request, user)
                    # print('logged in after 004')
                    # return render(request, 'home.html', {'is_active': is_active_verify})
                    if user:
                        print('004')
                        is_active_verify = False
                        login(request, user)
                        print('logged in after 004')
                        return render(request, 'home.html', {'is_active': is_active_verify})
                    else:
                        print('005')
                        error = 1
                        return render(request, 'login.html', {'error': error})

            else:
                incorrect_credentials = 1
                return render(request,'login.html', {'incorrect' : incorrect_credentials})


           

   return render(request, 'login.html', {'error': error})



def user_logout(request):
   logout(request)
   return render(request,'login.html')
