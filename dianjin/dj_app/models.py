from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

#新浪
class xinlang(models.Model):
    c_id = models.CharField(max_length=50,unique=True)   #新浪给的id
    c_time = models.CharField(max_length=50)
    c_title = models.CharField(max_length=500)
    now_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    pic = models.CharField(max_length=500)
    style = models.CharField(max_length=50,default='其他')

#多玩
class duowan(models.Model):
    c_id = models.CharField(max_length=50,unique=True)   #新浪给的id
    c_time = models.CharField(max_length=50)
    c_title = models.CharField(max_length=500)
    now_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    pic = models.CharField(max_length=500)
    style = models.CharField(max_length=50,default='其他')

#虎扑
class hupu(models.Model):
    c_id = models.CharField(max_length=50,unique=True)   #新浪给的id
    c_time = models.CharField(max_length=50)
    c_title = models.CharField(max_length=500)
    now_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    pic = models.CharField(max_length=500)
    style = models.CharField(max_length=50,default='其他')


