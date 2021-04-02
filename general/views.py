from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from functools import reduce
import operator
from django.db.models import Q
from .models import *
from .form import *
# Create your views here.
def home(request):
    organizations = Organization.objects.all()
    return render(request,'general/home.html',{'organizations':organizations})

def result(request):
    organizations = Organization.objects.all()
    if request.method =='POST':
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
        if queryList: organizations = Organization.objects.filter(reduce(operator.and_, queryList))

    context = {'organizations':organizations}
    return render(request, 'general/result.html', context)

def detail(request, orgId):
    organization = Organization.objects.get(id=orgId)
    comments = organization.comment_set.all()
    comments_count = comments.count()
    context = {'organization':organization,'comments':comments, 'comments_count':comments_count}

    return render(request,'general/detail.html',context)

def createComment(request, orgId):
    form = CreateCommentForm(initial={'organization':orgId})
    if request.method =='POST':
        #print(F"Post!! {request.POST}")
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            form.save()
            orgId = request.POST["organization"]
            return redirect(f'../detail/{orgId}')

    context = {"form" : form}
    return render(request,'general/createComment.html', context)

def updateComment(request, pk):
    comment = Comment.objects.get(id=pk)
    form  = CommentForm(instance=comment)

    if request.method =='POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            orgId = request.POST["organization"]
            return redirect(f'../detail/{orgId}')

    context = {"form" : form}
    return render(request,'general/commentForm.html', context)

def deleteComment(request):
    if request.method =='POST':
        cmtId = request.POST.get("cmtId", "")
        comment = Comment.objects.get(id=cmtId)

        comment.delete()
        data = {'success': f" Success delete id ='{ cmtId }' comment !!" }
        return JsonResponse(data)