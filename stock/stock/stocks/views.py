from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from userinfo.models import *
from deal.models import *
from .data import  *
import json
from .models import *
import logging


# Create your views here.

# k线数据
def k_data(request):
    k_data = stock_k_data()
    datastr = ''
    for idx in k_data.index:
        rowstr = '[\"%s\", %s, %s, %s, %s, %s]' % (idx, k_data.ix[idx]['open'],
                                           k_data.ix[idx]['close'], k_data.ix[idx]['low'],
                                           k_data.ix[idx]['high'], k_data.ix[idx]['volume'])
        datastr += rowstr + ','
    datastr = datastr[:-1]
    return HttpResponse(datastr)


#头部数据调用
def realHead(request,template):
    if template == 'index':
        df = stock_A()
    else:
        df = stock_company(template)
    price = "%.2f"%(float(df.price[0]))
    open_price = "%.2f"%(float(df.open[0]))
    high = "%.2f"%(float(df.high[0]))
    low = "%.2f"%(float(df.low[0]))
    pre_close = "%.2f"%(float(df.pre_close[0]))
    volume = "%.2f"%(float(df.volume[0]) / 100000000)
    amount = "%.2f"%(float(df.amount[0]) / 100000000)
    change = "%.2f"%(float(price) - float(pre_close))
    perce = "%.2f"%(float(change) / float(pre_close) * 100)
    return render(request,'realHead.html',locals())


# 热点资讯
def hotInfo(request):
    news = stock_news()[:8]
    news_title = serializers.serialize('json', news.title)
    return HttpResponse(news_title)


# 指数排行
def indexRang(request):
    index = stock_index()[:8]
    a =zip(index.name,index.change)
    b = []
    for i in a:
        c={}
        c['name'] = i[0]
        c['change'] = i[1]
        b.append(c)
    return HttpResponse(json.dumps(b))


# 实时解盘
def breakUp(request):
    bread_up = stock_breakup()[:5]
    # print(type(bread_up))
    ba = zip(bread_up.title, bread_up.time, bread_up.url)
    bb = []
    for i in ba:
        bc={}
        bc['title'] = i[0]
        bc['time'] = i[1]
        bc['url'] = i[2]
        bb.append(bc)
    return HttpResponse(json.dumps(bb))


# 自选股
def selfStock(request, stockNo):
    user = UserInfo.objects.filter(id=request.user.id)
    if len(user) > 0:
        stock = Stock.objects.filter(number=stockNo)
        SelfStock.objects.create(user=user[0].id, stock=stock[0].id)
        try:
            selfstock = SelfStock.objects.filter(user_id=request.user.id)
            if len(selfstock) > 0:
                data = serializers.serialize(selfstock)
                return HttpResponse(json.dumps({"result": False, "data": data, "error": ""}))
            else:
                return HttpResponse(json.dumps({"result": False, "data": "", "error": "该用户尚未添加自选股"}))
        except BaseException as e:
            logging.warning(e)
    else:
        return HttpResponse(json.dumps({"result":False, "data":"", "error":"去登录"}))
