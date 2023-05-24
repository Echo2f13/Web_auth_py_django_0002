from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())
  

def sign_up_page(request):
  return render(request,'regpage.html')

def log_in_page(request):
  return render(request,'login.html')