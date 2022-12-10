from django.db import models

# Create your models here.
class Customer(models.Model):
    CUSTOMER_ID = models.CharField(max_length=20)
    CUSTOMER_PW = models.CharField(max_length=40)
    CUSTOMER_NAME = models.CharField(max_length=40)
    CUSTOMER_BIRTH = models.CharField(max_length=8)
    CUSTOMER_PHONE = models.CharField(max_length=15)
    CUSTOMER_EMAIL = models.EmailField()
    CUSTOMER_ZIPCODE = models.CharField(max_length=10, default='')
    CUSTOMER_ADDR = models.CharField(max_length=300)
    FIRST_VISIT = models.DateTimeField(auto_now_add=True)
    LAST_VISIT = models.DateTimeField(auto_now=False)
    VISIT_CNT = models.IntegerField(default=0)
    CUSTOMER_RATING = models.ForeignKey('Rating', on_delete=models.DO_NOTHING, default=0)
    CUSTOMER_SEX = models.IntegerField(default=0)
    CRTIME = models.DateTimeField(auto_now=True)
    DISCARD = models.BooleanField(default=False)

class Rating(models.Model):
    NAME = models.CharField(max_length=20)
    ORDER = models.IntegerField(default=0)
    DISCARD = models.BooleanField(default=False)

class Goods(models.Model):
    NAME = models.CharField(max_length=200)
    TYPE = models.ForeignKey('GoodsType', on_delete=models.DO_NOTHING)
    BARCODE = models.CharField(max_length=100, default='')
    PRICE = models.IntegerField(default=0)
    CRTIME = models.DateTimeField(auto_now=True)
    DISCARD = models.BooleanField(default=False)

class GoodsType(models.Model):
    NAME = models.CharField(max_length=100)
    DISCARD = models.BooleanField(default=False)
