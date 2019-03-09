from django.db import models
from userinfo.models import *
from sale.models import *
# Create your models here.
# 购买意愿表Cart
class Cart(models.Model):
    # 用户表　
    # ForeignKey可能报错的地方版本不同添加on_delete=models.CASCADE
    user=models.ForeignKey(UserInfo)
    # 车辆信息表
    car=models.ForeignKey(CarInfo)
    price=models.DecimalField('价格',max_digits=10,decimal_places=2)
    def __str__(self):
        return self.user.username
#
# 订单表Order 日期和时间参数不同
class Order(models.Model):
    order_date=models.DateTimeField('交易时间',auto_now_add=True)
    # 交易价格Decimal / C
    price=models.DecimalField('交易价格',max_digits=10,decimal_places=2)
    orderNo=models.CharField('订单号',max_length=50,null=False)
    sale_user=models.ForeignKey(UserInfo,related_name='suser',on_delete=models.CASCADE)
    buy_user=models.ForeignKey(UserInfo,related_name='buser')
    def __str__(self):
        return self.orderNo

# Orderdetails
class Orderdetails(models.Model):
    order=models.ForeignKey(Order)
    brand=models.ForeignKey(Brand)
    ctitle = models.CharField('车辆名称', max_length=50, null=False)
    regist_date = models.DateField('上牌日期')
    engineNo = models.CharField('发动机号', max_length=50, null=False)
    mileage = models.IntegerField('公里数', default=0)
    maintenance_record = models.TextField('维修记录')
    price = models.DecimalField('期望售价', decimal_places=2, max_digits=10)
    extreactprice = models.DecimalField('成交价格', decimal_places=2, max_digits=10)
    newprice = models.DecimalField('新车价格', decimal_places=2, max_digits=10)
    picture = models.ImageField('图片', upload_to='img/car', default='normal.png')
    debt = models.CharField('债务', choices=DEBT_CHOICES, default='无', max_length=20)
    other = models.TextField('第三方评估')
    promise = models.TextField('卖家承诺')
    def __str__(self):
        return self.order.orderNo
