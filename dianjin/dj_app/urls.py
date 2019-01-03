from django.urls import path
from . import views

urlpatterns = [
    path('xinlang', views.xinlang, name='xinlang'),
    #path('hupu', views.hupu, name='hupu'),
    path('duowan', views.duowan, name='duowan'),

]