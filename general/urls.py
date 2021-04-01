from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('result/',views.result, name='result'),
    path('detail/<str:orgId>/',views.detail, name='detail'),
    path('commentForm/',views.createComment, name='createComment'),
    path('commentForm/<str:pk>',views.updateComment, name='updateComment')
]
