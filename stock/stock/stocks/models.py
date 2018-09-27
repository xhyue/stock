from django.db import models

# Create your models here.

class Stock(models.Model):
    number = models.IntegerField(verbose_name='股票编码')
    company_name = models.CharField(max_length=64, verbose_name='公司名称')
    area = models.CharField(max_length=30, blank=True, null=True, verbose_name='所属区域')
    update = models.DateField(verbose_name='上市日期')
    concepts = models.CharField(blank=True, null=True, max_length=200, verbose_name='涉及概念')
    main_business = models.CharField(blank=True, null=True, max_length=200, verbose_name='主营业务')
    per_net_asset = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='每股净资产')
    per_profit = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='每股收益')
    net_profit = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='净利润')
    net_profit_growth_rate = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='净利润增长率')
    income = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='营业收入')
    per_net_cash_flow = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='每股现金流')
    per_net_fund = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='每股公积金')
    per_net_unprofit = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='每股未分配利润')
    total_money = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='总股本')
    flow_money = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name='流通股')

    def __str__(self):
        return str(self.number)

    class Meta:
        db_table = 'Stock'
        verbose_name = '股票信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Link(models.Model):
    title = models.CharField(max_length=50,blank=True, null=True, verbose_name='标题')
    callback_url = models.URLField(blank=True, null=True, verbose_name='url地址')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.title

