from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
    organizations = Organization.objects.all()
    return render(request,'general/home.html',{'organizations':organizations})

def result(request):
    organizations = Organization.objects.all()
    return render(request,'general/result.html', {'organizations':organizations})

def detail(request):
    return render(request,'general/detail.html')