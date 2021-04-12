from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutPage, name='logout'),
    path('userSetting/',views.userSetting, name='userSetting'),

    path('',views.home, name='home'),
    path('result/',views.result, name='result'),
    path('detail/<str:orgId>/',views.detail, name='detail'),

    path('createComment/<str:orgId>',views.createComment, name='createComment'),
    path('commentForm/<str:pk>',views.updateComment, name='updateComment'),
    path('deleteComment',views.deleteComment, name='deleteComment'),

    #Reset Password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='general/resetSent.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='general/resetSentSuccess.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='general/resetPassword.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='general/resetSuccess.html'), name='password_reset_complete'),

    #Dev
    path('randomAddUser/',views.randomAddUser, name='randomAddUser'),
    path('addOrganization/',views.addOrganization, name='addOrganization'),
    
]
