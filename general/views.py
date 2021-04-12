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
@isLoginRedirect
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, f"伙伴 '{username}' 已經被註冊過了～請使用別的稱呼")
            return redirect('register')
        tmp = request.POST.copy()
        tmp['username'] = tmp['username'].lower()
        form = CreateUserForm(tmp)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"伙伴 '{username}' 註冊成功！現在可以登入嚕～")
            return redirect('login')

    context = {'form':form}
    return render(request,'general/register.html',context)

@isLoginRedirect
def loginPage(request):
    form = LoginUserForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request,username=username.lower(), password=password)
        if not User.objects.filter(username__iexact=username).exists():
            messages.error(request, f"稱呼 '{username}' 不存在，請先註冊。")
            return redirect('login')
        elif user is None:
            messages.error(request, f"稱呼 '{username}' 密碼不正確，請檢查後再嘗試。")
            return redirect('login')
        elif user.is_active:
            login(request, user)
            return redirect('home')


    context = {'form':form}
    return render(request,'general/login.html',context)

@isLogin
def userSetting(request):
    internPerson = InternPerson.objects.get(user=request.user)
    form = UpdateUserForm(instance=internPerson)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST,request.FILES, instance=internPerson)
        if form.is_valid():
            messages.success(request, f"你的資料更新成功嚕！～")
            form.save()
        
    context = {'internPerson':internPerson, 'form':form }
    return render(request,'general/userSetting.html',context)

def logoutPage(request):
    userName = request.user.username
    logout(request)
    messages.success(request, f"伙伴 '{userName}' 已經登出嚕，我們下次見～")
    return redirect('login')

def home(request):
    internPerson = {}
    if request.user.is_authenticated:
        internPerson = InternPerson.objects.get(user=request.user)
    organizations = Organization.objects.all()
    context = {'organizations':organizations, 'internPerson':internPerson}
    return render(request,'general/home.html', context)

def result(request):
    internPerson = {}
    if request.user.is_authenticated:
        internPerson = InternPerson.objects.get(user=request.user)
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
        
    context = {'organizations':organizations, 'internPerson':internPerson}
    return render(request, 'general/result.html', context)

@isAuthenticated_detail
#@allowed_user_groups(allowed_roles=['admin'])
def detail(request, orgId):
    internPerson = InternPerson.objects.get(user=request.user)
    organization = Organization.objects.get(id=orgId)
    comments = organization.comment_set.all()
    comments_count = comments.count()
    context = {'organization':organization,'internPerson':internPerson, 'comments':comments, 'comments_count':comments_count}
    return render(request,'general/detail.html',context)

@login_required(login_url='login')
def createComment(request, orgId):
    # TODO - Get UserId from Login
    internPerson = InternPerson.objects.get(user=request.user)
    form = CommentForm(initial={'organization':orgId, 'intern':internPerson.id})
    if request.method =='POST':
        print(F"Post!! {request.POST}")
        print(F"request.POST['hashTags']: {request.POST['hashTags']}")
        """
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            orgId = request.POST["organization"]
            updateRelatedFieldForOrganization(orgId)
            return redirect(f'../detail/{orgId}')
"""
    context = {"form" : form, 'internPerson': internPerson }
    return render(request,'general/commentForm.html', context)

@login_required(login_url='login')
def updateComment(request, pk):
    internPerson = InternPerson.objects.get(user=request.user)
    comment = Comment.objects.get(id=pk)
    form  = CommentForm(instance=comment)

    if request.method =='POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            orgId = request.POST["organization"]
            updateRelatedFieldForOrganization(orgId)
            return redirect(f'../detail/{orgId}')

    context = {"form" : form, 'internPerson':internPerson }
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

# Maintainance Purpose
import random
from .tests import test_names, user_pw_dev
def randomAddUser(request):
    if not request.user.is_staff:
        messages.error(request, f"伙伴 '{request.user}' 不是管理者，無權限進行此操作")
        return redirect('home')
    chkList = {}
    cnt = 0
    maxCnt = 25
    while cnt < maxCnt:
        index = random.randint(0,len(test_names)-1)
        name = test_names[index] +'_dev'
        if name not in chkList:
            cnt += 1
            chkList[name] =  {
                'username': name, 
                'email': name + '@testInternship1234.com', 
                'password1': user_pw_dev,
                'password2': user_pw_dev
            }
            print(F"chkList[name]: {chkList[name]}")
            form = CreateUserForm(chkList[name])
            if form.is_valid():
                print(F"form.is_valid: {name}")
                #print(F"form: {form}")
                #user = form.save()
    return redirect('login')

import json
from .tests import organization_dev
def addOrganization(request):
    if not request.user.is_staff:
        messages.error(request, f"伙伴 '{request.user}' 不是管理者，無權限進行此操作")
        return redirect('home')
    chkList = {}
    cnt = 0
    maxCnt = 25
    """
    organizationsInDB = Organization.objects.all()
    for org in organizationsInDB:
        if org.name not in chkList:
            chkList[org.name] = org.name
    print(f"chkList: {chkList}")
    """
    for org_name, orgInfo in organization_dev['Organization'].items():
        if cnt == maxCnt: break
        name = orgInfo['1. 機構名稱：']
        if name not in chkList:
            chkList[name] =  name
            print(F"chkList[org_name]: {chkList[name]}")
            org = Organization.objects.create(name=name)
            org.area= orgInfo['2. 地址：']
            org.organizationType = orgInfo['8. 實習機構類別：']
            org.score=  0
            org.commentsCount= 0
            org.unitName= orgInfo['3. 實習單位名稱：']
            org.unitType= orgInfo['8. 實習機構類別：']
            org.subsidy= orgInfo['實習津貼']
            org.internshipContent= orgInfo['2. 實習內容：']
            org.detailInfoFromExtUrl = ''
            org.save()
            print(f"------------")
        cnt += 1
    return redirect('login')
    """
    
    """