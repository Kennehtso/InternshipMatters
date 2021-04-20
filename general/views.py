from django.db.models.expressions import OrderBy
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.list import ListView
from django.core.paginator import Paginator

#Other import
from functools import reduce
import operator
from .models import *
from .form import *
from .decorators import *
from bs4 import BeautifulSoup
import requests
import re
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
    bannerSearch = ''
    location_list = ''
    organizationType_list = ''
    score_input = 0
    commentsCount_input = 0
    isApprove_input = 'all'
    print('------------------------------request.session before ------------------------------')
    if "bannerSearch" in request.session: bannerSearch = request.session["bannerSearch"]
    if "location_list" in request.session: location_list = request.session["location_list"] 
    if "organizationType_list" in request.session: organizationType_list = request.session["organizationType_list"] 
    if "score_input" in request.session: score_input = request.session["score_input"]  
    if "commentsCount_input" in request.session: commentsCount_input = request.session["commentsCount_input"]
    if "isApprove_input" in request.session: isApprove_input = request.session["isApprove_input"]
    
    if request.method =='POST':
        print(F"----------------- GET INTO POST =================")
        request.session["bannerSearch"] =''
        request.session["location_list"] =''
        request.session["organizationType_list"] = ''
        request.session["score_input"] = 0
        request.session["commentsCount_input"] = 0
        request.session["isApprove_input"] ='all'
        #print(f"*********　request.POST: {request.POST} ********** ")
        queryList = []
        # Combine Filter option
        if 'bannerSearch' in request.POST and request.POST['bannerSearch'] != '': 
            queryList.append(Q(name__icontains=request.POST['bannerSearch']))
            bannerSearch = request.POST['bannerSearch']
            request.session["bannerSearch"] = bannerSearch

        if 'location_list' in request.POST and request.POST['location_list'] != '': 
            queryList.append(Q(area__icontains=request.POST['location_list']))
            location_list = request.POST['location_list']
            request.session["location_list"] = location_list

        if 'organizationType_list' in request.POST and request.POST['organizationType_list'] != '': 
            queryList.append(Q(organizationType=request.POST['organizationType_list']))
            organizationType_list = request.POST['organizationType_list']
            request.session["organizationType_list"] = organizationType_list

        if 'score_input' in request.POST and request.POST['score_input']!= 0 : 
            queryList.append(Q(score__gte=request.POST['score_input']))
            score_input = request.POST['score_input']
            request.session["score_input"] = score_input

        if 'commentsCount_input' in request.POST and request.POST['commentsCount_input']!= 0 : 
            queryList.append(Q(commentsCount__gte=request.POST['commentsCount_input']))
            commentsCount_input = request.POST['commentsCount_input']
            request.session["commentsCount_input"] = commentsCount_input

        #print(F"request.POST['isApprove_input']: {request.POST['isApprove_input']}")
        if 'isApprove_input' in request.POST and request.POST['isApprove_input'] == 'true' : 
            queryList.append(Q(isApprove=True))
            isApprove_input = 'true'
            request.session["isApprove_input"] = isApprove_input
        elif 'isApprove_input' in request.POST and request.POST['isApprove_input'] == 'false' : 
            queryList.append(Q(isApprove=False))
            isApprove_input = 'false'
            request.session["isApprove_input"] = isApprove_input

        # Fetch actopm
        if queryList: 
            organizations = Organization.objects.filter(reduce(operator.and_, queryList))
    else:
        print(F"----------------- GET INTO INFINITE, USE SESSION =================")
        #print(f"*********　request.POST: {request.POST} ********** ")
        queryList = []
        # Combine Filter option
        if 'bannerSearch' in request.session and request.session['bannerSearch'] != '': 
            queryList.append(Q(name__icontains=request.session['bannerSearch']))

        if 'location_list' in request.session and request.session['location_list'] != '': 
            queryList.append(Q(area__icontains=request.session['location_list']))

        if 'organizationType_list' in request.session and request.session['organizationType_list'] != '': 
            queryList.append(Q(organizationType=request.session['organizationType_list']))

        if 'score_input' in request.session and request.session['score_input']!= 0 : 
            queryList.append(Q(score__gte=request.session['score_input']))

        if 'commentsCount_input' in request.session and request.session['commentsCount_input']!= 0 : 
            queryList.append(Q(commentsCount__gte=request.session['commentsCount_input']))

        if 'isApprove_input' in request.session and request.session['isApprove_input'] == 'true' : 
            queryList.append(Q(isApprove=True))
        elif 'isApprove_input' in request.session and request.session['isApprove_input'] == 'false' : 
            queryList.append(Q(isApprove=False))

        # Fetch actopm
        if queryList: 
            organizations = Organization.objects.filter(reduce(operator.and_, queryList))

    organizations_count = organizations.count()
    #Implement paginator
    paginator = Paginator(organizations.order_by('name'), 12) # Show 25 contacts per page.
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'internPerson':internPerson,'page_obj': page_obj,'organizations_count': organizations_count,
    'bannerSearch':bannerSearch,'location_list':location_list,'organizationType_list':organizationType_list,'score_input':score_input,
    'commentsCount_input':commentsCount_input,'isApprove_input':isApprove_input,
    }
    return render(request, 'general/result.html', context)

def getElementsByUrl(url):
    try:
        resp = requests.get(url,headers={"User-Agent": "curl/7.61.0"})
        resp.encoding = 'big5'
        soup = BeautifulSoup(resp.text,"html.parser")
        return soup
    except:
        return None

def getDetailData(url_detail, name=None ):
    data = {}
    detailPage = url_detail #f"http://internship.guidance.org.tw/internship_sheet.php{url_detail}"
    data['資料來源'] = detailPage
    soup = getElementsByUrl(detailPage)
    if soup is None:
        return None
    table = soup.find('table', attrs={'id':'table2'})
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 2:
            continue
        if len(cols) == 2:
            f0 = re.sub(r"\s+"," ", re.sub(r"^\s+|\s+$", "", re.sub(r'(\u3000)|(\xa0)', '', re.sub(r'(\t)|(\n)|(\r)', '', cols[0].text))))  
            f1 = re.sub(r"\s+"," ", re.sub(r"^\s+|\s+$", "", re.sub(r'(\u3000)|(\xa0)', '', re.sub(r'(\t)|(\n)|(\r)', '', cols[1].text))))
            data[f0]  = f1
            #if f0 == "2. 地址：":
            #    data["坐標"] = getGeoByHERE(name, f1)
        elif len(cols) == 3:
            f1 = re.sub(r"\s+"," ", re.sub(r"^\s+|\s+$", "", re.sub(r'(\u3000)|(\xa0)', '', re.sub(r'(\t)|(\n)|(\r)', '', cols[1].text))))
            f2 =re.sub(r"\s+"," ", re.sub(r"^\s+|\s+$", "", re.sub(r'(\u3000)|(\xa0)', '', re.sub(r'(\t)|(\n)|(\r)', '', cols[2].text))))
            data[f1]  = f2 
    return data

@isAuthenticated_detail
#@allowed_user_groups(allowed_roles=['admin'])
def detail(request, orgId):
    internPerson = InternPerson.objects.get(user=request.user)
    organizations = Organization.objects.all()
    organization = Organization.objects.get(id=orgId)
    organizationDetail = getDetailData(organization.detailInfoFromExtUrl)
    organizationDetailObj = {
        'unitName' : organizationDetail['3. 實習單位名稱：'],
        'address' : organizationDetail['2. 地址：'],
        'telephone' : organizationDetail['6. 聯絡電話：'],
        'email' : organizationDetail['7. 電子信箱：'],
        'internshipType' : organizationDetail['8. 實習機構類別：'],
        'subsidy' : organizationDetail['實習津貼'],
        'personalSupervise' : organizationDetail['個別督導'],
        'consultingRoom' : organizationDetail['個諮室'],
        'consultingRoomForGroup' : organizationDetail['團輔室'],
        'numbersOfCases' : organizationDetail['每位全職實習生平均每週接案人數'],
        'numbersOffullTime' : organizationDetail['專任心理師人數'],
        'facilities' : organizationDetail['辦公室（桌椅）'],
        'internshipContent' : organizationDetail['2. 實習內容：'],
        'superviser' : organizationDetail['4. 實習單位主管：'],
        'officer' : organizationDetail['5. 承辦人：'],
        'supervise' : organizationDetail['諮商心理師提供之督導'],
        'groupSupervise' : organizationDetail['團體督導或研習'],
    }
    comments = organization.comment_set.all()
    comments_count = comments.count()
    context = {'organizations':organizations, 'organization':organization,'internPerson':internPerson, 'comments':comments, 'comments_count':comments_count, 'organizationDetailObj':organizationDetailObj}
    return render(request,'general/detail.html',context)

@login_required(login_url='login')
def createComment(request, orgId):
    # TODO - Get UserId from Login
    internPerson = InternPerson.objects.get(user=request.user)
    form = CommentForm(initial={'organization':orgId, 'intern':internPerson.id})
    if request.method =='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            hashTags = form.cleaned_data.get('hashTags')
            orgId = request.POST["organization"]
            updateRelatedFieldForOrganization(orgId, hashTags)
            return redirect(f'../detail/{orgId}')

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
            orgId = request.POST["organization"]
            form.save()
            hashTags = form.cleaned_data.get('hashTags')
            orgId = request.POST["organization"]
            updateRelatedFieldForOrganization(orgId, hashTags)
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
        updateRelatedFieldForOrganization(orgId)
        data = {'success': f" Success delete id ='{ cmtId }' comment !!" }
        return JsonResponse(data)

def updateRelatedFieldForOrganization(orgId, hashTags=None):
    print(F"hashTags: {hashTags}")
    organization = Organization.objects.get(id=orgId)
    comments = Comment.objects.filter(organization__id=orgId)
    organization.commentsCount = comments.count()
    avgScore = comments.aggregate(Avg('score'))["score__avg"]
    organization.score = 0 if avgScore is None else round(avgScore,1)
    
    hashTag_u = hashTags if hashTags is not None else HashTags.objects.none()
    for cmt in comments:
        hashTag_u = hashTag_u.union(cmt.hashTags.all())
    organization.hashTags.clear()
    for h in hashTag_u.all():
        organization.hashTags.add(h)
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
    maxCnt = 30
    for org_name, orgInfo in organization_dev['Organization'].items():
        #if cnt == maxCnt: break
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
            org.detailInfoFromExtUrl = orgInfo['資料來源']
            org.save()
            print(F"{chkList[name]}: Save success")
            print(f"------------")
        #cnt += 1
    return redirect('login')