from email.policy import default
from django.db import models

# Create your models here.
class User(models.Model):
    USER_ID = models.CharField(max_length=20)
    USER_PW = models.CharField(max_length=200, default='')
    USER_NAME = models.CharField(max_length=40)
    USER_BIRTH = models.CharField(max_length=8)
    USER_PHONE = models.CharField(max_length=15)
    USER_EMAIL = models.EmailField()
    CRTIME = models.DateTimeField(auto_now=True)
    DISCARD = models.BooleanField(default=False)
