from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('Home page')

def result(request):
    return HttpResponse('Result page')

def detail(request):
    return HttpResponse('Detail page')