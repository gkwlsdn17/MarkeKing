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

    def __str__(self):
        return f'''
        customer_table_id={self.id}, CUSTOMER_ID={self.CUSTOMER_ID}, 
        CUSTOMER_NAME={self.CUSTOMER_NAME}, CUSTOMER_BIRTH={self.CUSTOMER_BIRTH}, 
        CUSTOMER_PHONE={self.CUSTOMER_PHONE}, CUSTOMER_EMAIL={self.CUSTOMER_EMAIL},
        CUSTOMER_ZIPCODE={self.CUSTOMER_ZIPCODE}, CUSTOMER_ADDR={self.CUSTOMER_ADDR},
        FIRST_VISIT={self.FIRST_VISIT}, LAST_VISIT={self.LAST_VISIT},
        CUSTOMER_SEX={self.CUSTOMER_SEX},
        CRTIME={self.CRTIME}, DISCARD={self.DISCARD}'''

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

class Order(models.Model):
    CUSTOMER_NO = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    ORDER_DATE = models.CharField(max_length=100, default='')
    TOTAL_AMOUNT = models.IntegerField(default=0)
    MEMO = models.CharField(max_length=1024, default='')
    CRTIME = models.DateTimeField(auto_now=True)
    DISCARD = models.BooleanField(default=False)
    CANCEL_DATE = models.CharField(max_length=100, default='', blank=True, null=True)
    
    def __str__(self):
        return f'''
        Order_table_id={self.id},
        CUSTOMER_NO={self.CUSTOMER_NO},
        ORDER_DATE={self.ORDER_DATE},
        TOTAL_AMOUNT={self.TOTAL_AMOUNT},
        MEMO={self.MEMO},
        CRTIME={self.CRTIME},
        DISCARD={self.DISCARD}
        '''

class Item(models.Model):
    ORDER_NO = models.ForeignKey('Order', on_delete=models.DO_NOTHING)
    GOODS_NO = models.ForeignKey('Goods', on_delete=models.DO_NOTHING)
    GOODS_NAME = models.CharField(max_length=200)
    GOODS_COUNT = models.IntegerField(default=0)
    PRICE = models.IntegerField(default=0)
    TOTAL_AMOUNT = models.IntegerField(default=0)
    DISCARD = models.BooleanField(default=False)

class Delivery(models.Model):
    ORDER_NO = models.ForeignKey('Order', on_delete=models.DO_NOTHING, default=0)
    CUSTOMER_NO = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    DELIVERY_DATE = models.CharField(max_length=100, default='', blank=True, null=True)
    ARRIVAL_DATE = models.CharField(max_length=100, default='', blank=True, null=True)
    DELIVERY_NAME = models.CharField(max_length=200)
    DELIVERY_ADDR = models.CharField(max_length=1024)
    DELIVERY_PHONE = models.CharField(max_length=100)
    DELIVERY_STATUS = models.ForeignKey('DeliveryStatus', on_delete=models.DO_NOTHING, default=1)
    DELIVERY_COMPANY = models.ForeignKey('DeliveryCompany', on_delete=models.DO_NOTHING, default=1)
    CRTIME = models.DateTimeField(auto_now=True)
    DISCARD = models.BooleanField(default=False)

    def __str__(self):
        return f'''
        CUSTOMER_NO={self.CUSTOMER_NO.id}
        ,DELIVERY_DATE={self.DELIVERY_DATE}
        ,ARRIVAL_DATE={self.ARRIVAL_DATE}
        ,DELIVERY_NAME={self.DELIVERY_NAME}
        ,DELIVERY_ADDR={self.DELIVERY_ADDR}
        ,DELIVERY_PHONE={self.DELIVERY_PHONE}
        ,DELIVERY_STATUS={self.DELIVERY_STATUS}
        ,DELIVERY_COMPANY{self.DELIVERY_COMPANY}
        ,CRTIME={self.CRTIME}
        ,DISCARD={self.DISCARD}
        '''

class DeliveryStatus(models.Model):
    STATUS = models.CharField(max_length=512)
    CRTIME = models.DateTimeField(auto_now=True)
    DISCARD = models.BooleanField(default=False)

class DeliveryCompany(models.Model):
    COMPANY_NAME = models.CharField(max_length=512)
    COMPANY_PHONE = models.CharField(max_length=100)
    CRTIME = models.DateTimeField(auto_now=True)
    DISCARD = models.BooleanField(default=False)