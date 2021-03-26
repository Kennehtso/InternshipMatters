from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
    return render(request,'general/home.html')

def result(request):
    return render(request,'general/result.html')

def detail(request):
    return render(request,'general/detail.html')