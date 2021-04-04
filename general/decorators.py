from django.http import HttpResponse
from django.shortcuts import redirect, render
from .form import *
from django.contrib import messages


def isAuthenticated_detail(views_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = LoginUserForm()
            context = {'form':form}
            messages.error(request, f"要先登入才能瀏覽 “機構評論詳閱” 頁面。")
            return redirect('login')
        return views_func(request, *args, **kwargs)
    return wrapper_func

def isLogin(views_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return views_func(request, *args, **kwargs)
    return wrapper_func

def allowed_user_groups(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('你沒有權限閱覽此頁面，請聯絡管理員。')
        return wrapper_func
    return decorator
