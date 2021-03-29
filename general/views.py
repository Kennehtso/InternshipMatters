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

def detail(request, orgId):
    organization = Organization.objects.get(id=orgId)
    comments = organization.comment_set.all()
    comments_count = comments.count()
    context = {'organization':organization,'comments':comments, 'comments_count':comments_count}

    return render(request,'general/detail.html',context)