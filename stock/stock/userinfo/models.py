from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from stocks.models import *
# Create your models here.


class UserInfo(AbstractUser):
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    email = models.CharField(max_length=30, blank=True, null=True, verbose_name='邮箱')
    identity = models.CharField(max_length=20, blank=True, null=True, verbose_name='身份证号')
    isactive = models.BooleanField(default=False, verbose_name='是否激活')
    isban = models.BooleanField(default=False, verbose_name='是否禁用')
    tradepwd = models.CharField(max_length=9, blank=True, null=True, verbose_name='交易密码')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Hold(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name='用户')
    stock = models.ForeignKey(Stock, verbose_name='股票')
    amount = models.IntegerField(blank=True, null=True, verbose_name='持有数量')
    frozen = models.IntegerField(blank=True, null=True, verbose_name='冻结股')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Hold'
        verbose_name = '持仓表'
        verbose_name_plural = verbose_name


class Fund(models.Model):
    user = models.OneToOneField(UserInfo, verbose_name='用户')
    money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='总资金')
    frozen_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='冻结资金')



    class Meta:
        db_table = 'Fund'
        verbose_name = '资金表'
        verbose_name_plural = verbose_name


class Bank(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name='用户')
    bank = models.CharField(max_length=40, verbose_name='开户行')
    bankNo = models.IntegerField(verbose_name='卡号')

    def __str__(self):
        return self.bank

    class Meta:
        db_table = 'Bank'
        verbose_name = '银行表'
        verbose_name_plural = verbose_name