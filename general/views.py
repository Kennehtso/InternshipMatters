from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

#Other import
from functools import reduce
import operator
from .models import *
from .form import *
from .decorators import *

# Create your views here.
@isLogin
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='internPerson')
            user.groups.add(group)


            messages.success(request, f"伙伴 '{username}' 註冊成功！現在可以登入嚕～")
            return redirect('login')

    context = {'form':form}
    return render(request,'general/register.html',context)

@isLogin
def loginPage(request):
    form = LoginUserForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request,username=username, password=password)
        if user is None:
            messages.error(request, f"稱呼 '{username}' 或密碼有誤，請檢查後再嘗試")
            return redirect('login')
        else:
            login(request, user)
            return render(request,'general/home.html')


    context = {'form':form}
    return render(request,'general/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    organizations = Organization.objects.all()
    return render(request,'general/home.html',{'organizations':organizations})

def result(request):
    organizations = Organization.objects.all()
    if request.method =='POST':
        #print(f"*********　request.POST: {request.POST} ********** ")
        queryList = []
        # Get Data
        bannerSearch = request.POST['bannerSearch']
        location = request.POST['location_list']
        organizationType = request.POST['organizationType_list']
        score_input = None
        commentsCount = None
        # Combine Filter option
        if bannerSearch and bannerSearch != '': 
            queryList.append(Q(name__icontains=bannerSearch))
        if location and location != '': 
            queryList.append(Q(area__icontains=location))
        if organizationType and organizationType != '': 
            queryList.append(Q(organizationType=organizationType))
        if 'score_input' in request.POST and request.POST['score_input']!= 0 : 
            queryList.append(Q(score__gte=request.POST['score_input']))
        if 'commentsCount_input' in request.POST and request.POST['commentsCount_input']!= 0 : 
            queryList.append(Q(commentsCount__gte=request.POST['commentsCount_input']))

        # Fetch actopm
        if queryList: 
            organizations = Organization.objects.filter(reduce(operator.and_, queryList))
        
    context = {'organizations':organizations}
    return render(request, 'general/result.html', context)

@isAuthenticated_detail
#@allowed_user_groups(allowed_roles=['admin'])
def detail(request, orgId):
    organization = Organization.objects.get(id=orgId)
    comments = organization.comment_set.all()
    comments_count = comments.count()
    context = {'organization':organization,'comments':comments, 'comments_count':comments_count}

    return render(request,'general/detail.html',context)

@login_required(login_url='login')
def createComment(request, orgId):
    # TODO - Get UserId from Login
    internPerson = InternPerson.objects.get(user=request.user)
    form = CommentForm(initial={'organization':orgId, 'intern':internPerson.id})
    if request.method =='POST':
        #print(F"Post!! {request.POST}")
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            orgId = request.POST["organization"]
            updateRelatedFieldForOrganization(orgId)
            return redirect(f'../detail/{orgId}')

    context = {"form" : form}
    return render(request,'general/commentForm.html', context)

@login_required(login_url='login')
def updateComment(request, pk):
    comment = Comment.objects.get(id=pk)
    form  = CommentForm(instance=comment)

    if request.method =='POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            orgId = request.POST["organization"]
            updateRelatedFieldForOrganization(orgId)
            return redirect(f'../detail/{orgId}')

    context = {"form" : form}
    return render(request,'general/commentForm.html', context)

@login_required(login_url='login')
def deleteComment(request):
    if request.method =='POST':
        cmtId = request.POST["cmtId"]
        orgId = request.POST["orgId"]

        comment = Comment.objects.get(id=cmtId)
        comment.delete()
        data = {'success': f" Success delete id ='{ cmtId }' comment !!" }
        return JsonResponse(data)

def updateRelatedFieldForOrganization(orgId):
    organization = Organization.objects.get(id=orgId)
    comments = Comment.objects.filter(organization__id=orgId)
    organization.commentsCount = comments.count()
    avgScore = comments.aggregate(Avg('score'))["score__avg"]
    organization.score = 0 if avgScore is None else round(avgScore,1)
    organization.save()