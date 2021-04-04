from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutPage, name='logout'),

    path('',views.home, name='home'),
    path('result/',views.result, name='result'),
    path('detail/<str:orgId>/',views.detail, name='detail'),
    path('createComment/<str:orgId>',views.createComment, name='createComment'),
    path('commentForm/<str:pk>',views.updateComment, name='updateComment'),
    path('deleteComment',views.deleteComment, name='deleteComment')
]
