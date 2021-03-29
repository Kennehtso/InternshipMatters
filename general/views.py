from django.shortcuts import render
from django.http import HttpResponse
from functools import reduce
import operator
from django.db.models import Q
from .models import *
# Create your views here.
def home(request):
    organizations = Organization.objects.all()
    return render(request,'general/home.html',{'organizations':organizations})

def result(request):
    queryList = []
    # Get Data
    bannerSearch = request.POST['bannerSearch']
    location = request.POST['location_list']
    internshipType = request.POST['internshipType_list']

    # Combine Filter option
    if bannerSearch and bannerSearch != '': 
        queryList.append(Q(name__icontains=bannerSearch))
    if location and location != '': 
        queryList.append(Q(area__icontains=location))
    #if internshipType: queryList.append(internshipType)

    # Fetch actopm
    if not queryList: organizations = Organization.objects.all()
    else: organizations = Organization.objects.filter(reduce(operator.and_, queryList))

    context = {'organizations':organizations}
    return render(request, 'general/result.html', context)

def detail(request, orgId):
    organization = Organization.objects.get(id=orgId)
    comments = organization.comment_set.all()
    comments_count = comments.count()
    context = {'organization':organization,'comments':comments, 'comments_count':comments_count}

    return render(request,'general/detail.html',context)