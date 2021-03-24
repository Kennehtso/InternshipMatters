from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path('home/',views.home),
    path('result/',views.result),
    path('detail/',views.detail),
]
