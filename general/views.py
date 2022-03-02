from sys import intern
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
from datetime import datetime
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

@isLogin
def applyOrganization(request):
    #TODO: Leave comments, happiness in the same time. 
    # those field will send mail to notice admin to initialize a first comment when create
    internPerson = InternPerson.objects.get(user=request.user)
    form = CreateOrganizationForm()

    if request.method == 'POST':
        form = UpdateUserForm(request.POST,request.FILES, instance=internPerson)
        if form.is_valid():
            messages.success(request, f"你的資料更新成功嚕！～")
            form.save()
        
    context = {'internPerson':internPerson, 'form':form }
    return render(request,'general/applyOrganization.html',context)

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
def qna(request):
    internPerson = {}
    if request.user.is_authenticated:
        internPerson = InternPerson.objects.get(user=request.user)
    context = {'internPerson':internPerson,}
    return render(request, 'general/qna.html', context)

def supportUs(request):
    internPerson = {}
    if request.user.is_authenticated:
        internPerson = InternPerson.objects.get(user=request.user)
    context = {'internPerson':internPerson,}
    return render(request, 'general/supportUs.html', context)


def noticesNews(request):
    internPerson = {}
    if request.user.is_authenticated:
        internPerson = InternPerson.objects.get(user=request.user)
    context = {'internPerson':internPerson,}
    return render(request, 'general/noticesNews.html', context)
    
def getElementsByUrl(url):
    try:
        resp = requests.get(url,headers={"User-Agent": "curl/7.61.0"} ,timeout=5)
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

#@isAuthenticated_detail
#@allowed_user_groups(allowed_roles=['admin'])
def detail(request, orgId):
        
    organizations = Organization.objects.all()
    organization = Organization.objects.get(id=orgId)
    """ Due to performance issues, not collcecting detail data
    organizationDetail =  getDetailData(organization.detailInfoFromExtUrl) # Currently not able to connnect with the website
    #print(F"organizationDetail: {organizationDetail}")
    organizationDetailObj = {
        'unitName' : '暫沒資料提供',
        'address' :'暫沒資料提供',
        'telephone' : '暫沒資料提供',
        'email' : '暫沒資料提供',
        'internshipType' : '暫沒資料提供',
        'subsidy' : '暫沒資料提供',
        'personalSupervise' :'暫沒資料提供',
        'consultingRoom' : '暫沒資料提供',
        'consultingRoomForGroup' :'暫沒資料提供',
        'numbersOfCases' : '暫沒資料提供',
        'numbersOffullTime' : '暫沒資料提供',
        'facilities' :'暫沒資料提供',
        'internshipContent' :'暫沒資料提供',
        'superviser' : '暫沒資料提供',
        'officer' : '暫沒資料提供',
        'supervise' :'暫沒資料提供',
        'groupSupervise' : '暫沒資料提供',
    }
    if organizationDetail is not None:
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
    """
    internPerson = None
    comments = organization.comment_set.all()
    comments_count = comments.count()
    commentMapVotes = {}
    if not request.user.is_anonymous:
        internPerson = InternPerson.objects.get(user=request.user)
        comments_ids = comments.values_list('id', flat=True)
        votesAll = Votes.objects.all()
        
        for comment in comments:
            vote = votesAll.filter(intern=internPerson, comment__id=comment.id)
            if not vote:
                tmpVote = Votes(intern=internPerson, voteType='neutral')
                tmpVote.save()
                comment.votes.add(tmpVote)

        votesForCurrentUser = votesAll.filter(intern=internPerson, comment__id__in=comments_ids)
        for vote in votesForCurrentUser:
            cmt_ByVote = vote.comment_set.first()
            if cmt_ByVote.id not in commentMapVotes:
                agreeCount = votesAll.filter(voteType='agree', comment__id=cmt_ByVote.id).count()
                neutralCount = votesAll.filter(voteType='neutral', comment__id=cmt_ByVote.id).count()
                disagreeCount = votesAll.filter(voteType='disagree', comment__id=cmt_ByVote.id).count()
                commentMapVotes[cmt_ByVote.id] = [vote.voteType, agreeCount, neutralCount, disagreeCount]

    context = {'organizations':organizations, 'organization':organization,'internPerson':internPerson, 'comments':comments, 'comments_count':comments_count, 
    #'organizationDetailObj':organizationDetailObj,
    'commentMapVotes':commentMapVotes,}
    return render(request,'general/detail.html',context)

#@login_required(login_url='login')
def createComment(request, orgId):
    if not request.user.is_authenticated:
        messages.warning(request, f"要先登入後才能進行分享哦～")
        return redirect(f'../detail/{orgId}')
    
    firstComment = Comment.objects.filter(organization__id=orgId, intern__user=request.user).first()
    if firstComment:
        messages.warning(request, f"伙伴 '{request.user.username}' 你已經對這個這個機構進行評價嚕 ('{firstComment.comments[:10]+'...' if len(firstComment.comments) > 10 else firstComment.comments }')。")
        return redirect(f'../detail/{orgId}')
    internPerson = InternPerson.objects.get(user=request.user)
    form = CommentForm(initial={'organization':orgId, 'intern':internPerson.id})
    if request.method =='POST':
        print(F"-----{request.POST}-----")
        form = CommentForm(request.POST)
        if form.is_valid():
            f = form.save()
            comment = Comment.objects.get(id=f.id)
            comment.updatedDate = datetime.now()
            comment.save()
            #Update hashtags
            hashTags_all = HashTags.objects.all()
            for text in request.POST.getlist('customHashTags'):
                #if text.isnumeric(): continue
                if not hashTags_all.filter(name__iexact=text).exists():
                    tmpTag = HashTags(name=text)
                    tmpTag.save()
                    comment.hashTags.add(tmpTag)
                    
            #Update Organization
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
    if internPerson.id != comment.intern.id:
        messages.error(request, f"伙伴 '{request.user.username}' 沒有該評論的修改權限哦。")
        return redirect(f'../detail/{comment.organization.id}')
    
    form  = CommentForm(instance=comment)
    if request.method =='POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            comment.updatedDate = datetime.now()
            comment.save()
            #Update hashtags
            hashTags_all = HashTags.objects.all()
            for text in request.POST.getlist('customHashTags'):
                #if text.isnumeric(): continue
                if not hashTags_all.filter(name__iexact=text).exists():
                    tmpTag = HashTags(name=text)
                    tmpTag.save()
                    comment.hashTags.add(tmpTag)

            #Update Organization
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
        
@login_required(login_url='login')
def updateCommentVote(request):
    if request.method =='POST':
        cmtId = request.POST["cmtId"]
        internPerson = InternPerson.objects.get(user=request.user)
        voteValue = request.POST["voteValue"]
            
        comment = Comment.objects.get(id=cmtId)
        vote = Votes.objects.filter(intern=internPerson, comment__id=cmtId).first()
        if not vote:
            tmpVote = Votes(intern=internPerson, voteType=voteValue)
            tmpVote.save()
            comment.votes.add(tmpVote)
            data = {'success': f" Create new Vote '{ tmpVote }' comment !!" }
        else:
            vote.voteType = voteValue
            vote.save()
            data = {'success': f" Update Vote '{ vote }' comment !!" }
            
        votesAll = Votes.objects.all()
        agreeCount = votesAll.filter(voteType='agree', comment__id=cmtId).count()
        neutralCount = votesAll.filter(voteType='neutral', comment__id=cmtId).count()
        disagreeCount = votesAll.filter(voteType='disagree', comment__id=cmtId).count()
        data['agreeCount'], data['neutralCount'], data['disagreeCount'] = agreeCount, neutralCount, disagreeCount
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


def getEmailTemplate(username, orgName, orgAddress):
    return f"<div style=\"margin:0;padding:0\" bgcolor=\"#FFFFFF\"> <table width=\"100%\" height=\"100%\" style=\"min-width:348px\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" lang=\"en\"> <tbody> <tr height=\"32\" style=\"height:32px\"> <td></td> </tr> <tr align=\"center\"> <td> <table border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"padding-bottom:20px;max-width:516px;min-width:220px\"> <tbody> <tr> <td width=\"8\" style=\"width:8px\"></td> <td> <div style=\"border-radius:8px;padding:40px 20px; border: 10px solid; border-image-slice: 1;border-width: 5px;border-image-source: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);\" align=\"center\" > <div style=\"font-family:\'Google Sans\',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;border-bottom:thin solid #dadce0;color:rgba(0,0,0,0.87);line-height:32px;padding-bottom:24px;padding-bottom:32px;text-align:center;word-break:break-word\"> <div style=\"font-size:24px\"> <table style=\"font-family:\'Google Sans\',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;font-size:24px;line-height:28px;text-align:center;width:100%\"> <tbody> <img src=\"https://upload.wikimedia.org/wikipedia/commons/d/d5/InternshipMatters_Logo.png\" width=\"74\" height=\"24\" aria-hidden=\"true\" style=\"margin-bottom:16px;background-color: #17a2b8;width: auto;height: 2em;border-radius: 0.25em;padding: 10px;\" alt=\"Google\" class=\"CToWUd\"> <tr> <td style=\"font-family:inherit\">感謝 {username}，我們已經收到你的提議！</td> </tr> </tbody> </table> </div> <table align=\"center\" style=\"margin-top:8px\"> <tbody> <tr style=\"line-height:normal\"> <td><a style=\"font-family:\'Google Sans\',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.87);font-size:14px;line-height:20px\">「{orgName}」({orgAddress}) </a> </td> </tr> </tbody> </table> </div> <div style=\"font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:rgba(0,0,0,0.87);line-height:20px;padding-top:20px;text-align:left\"> <table style=\"font-size:14px;letter-spacing:0.2;line-height:20px;text-align:center\"> <tbody> <tr> <td style=\"padding-bottom:24px;text-align:center\"> 屆時我們將收集相關的資訊， <div style=\"height:13px\"></div> 經確認無誤後便會把「{orgName}」加入至系統。 <div style=\"height:13px\"></div> 待更新完成後會發信通知，之後便可以進行討論跟分享了！ <div style=\"height:13px\"></div> 這段時間再麻煩你耐心等候，謝謝 </td> </tr> </tbody> </table> </div> </div> <div style=\"text-align:center\"> <div style=\"font-family:Roboto-Regular,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.54);font-size:11px;line-height:18px;padding-top:12px;text-align:center\"> <div>這是系統發出的通知，請不要回覆此信件</div> <div style=\"direction:ltr\">© Internship Matters! 2021. All Rights Reserved. <a href=\"mailto:internshipsmatters@gmail.com\" style=\"font-family:Roboto-Regular,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.54);font-size:11px;line-height:18px;padding-top:12px;text-align:center\">internshipsmatters@gmail.com </a></div> </div> </div> </td> <td width=\"8\" style=\"width:8px\"></td> </tr> </tbody> </table> </td> </tr> <tr height=\"32\" style=\"height:32px\"> <td></td> </tr> </tbody> </table> </div>"

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
def sendmailApplyNewOrganization(request):
    if request.method =='POST':
        orgName = request.POST["organization_new"]
        orgAddress = request.POST["address_new"]
        if orgName =='' or orgAddress == '':
            #messages.warning(request, f"提議加入的機構名稱及地均不能是空的哦")
            
            data = {'fail': f" 提議加入的機構名稱及地均不能是空的哦 !!" }
            return JsonResponse(data)
            #return redirect('result')

        subject, from_email, toList = F'InternshipMatters-提議新增-{orgName}','nternshipsmatters@gmail.com' , [request.user.email, 'nternshipsmatters@gmail.com']
        text_content = '感謝你的提議.'
        html_content = getEmailTemplate(request.user.username, orgName, orgAddress)
        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to=toList)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            #messages.success(request, f"機構 '{orgName}' 新增的提議已經發送嚕，經過確認後會再更新至系統，謝謝你的提議～")
            data = {'success': f"機構 '{orgName}' 新增的提議已經發送嚕，經過確認後會再更新至系統，謝謝你的提議～" }
        except Exception as e:
            print(f'[Exception Send mail] - ({type(e)}): {e}')
            #messages.error(request, f"系統異常，機構 '{orgName}'新增的提議未能發送至信箱，請稍後再試。如屢次發送失敗或可以透過Email與我們聯繫。")
            data = {'fail': f"系統異常，機構 '{orgName}'新增的提議未能發送至信箱，請稍後再試。如屢次發送失敗或可以透過Email與我們聯繫。" }
        
        return JsonResponse(data)
        #return redirect('result')
# Maintainance Purpose

#import random
#from .tests import test_names, user_pw_dev
def randomAddUser(request):
    """
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
    """
    return redirect('login')

#import json
#from .tests import organization_dev
def addOrganization(request):
    """
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
    """
    return redirect('login')