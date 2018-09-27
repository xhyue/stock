from django.shortcuts import render
from django.http import HttpResponse
from userinfo.models import *
from django.db.models import F
from .models import *
import json
import datetime
# Create your views here.


def deal(request, user, sob, stockNo, amount, price, price_range):
    if sob == "sale":
        hold = Hold.objects.filter(user_id=user.id,stock_number=stockNo)
        fund = Fund.objects.filter(user_id=user.id)
        new_amount = hold[0].amount - hold[0].frozen
        stock = Stock.objects.get(number=stockNo)
        stockdetail = json.dumps(stock)
        datetimes = datetime.datetime.now()
        if new_amount >= amount:
            # 将要卖股票进行冻结
            hold[0].frozen = hold[0].frozen + amount
            hold.save()
            # 查询全部买入
            buy_stock = BOSStock.objects.filter(stock_number=stockNo,role=0,price__range=(price,price+price_range))
            if len(buy_stock)<=0:
                bosstock = BOSStock()
                bosstock.user = user
                bosstock.stock = stock
                bosstock.role = 1
                bosstock.price = price
                bosstock.amount = amount
                bosstock.datetime = datetimes
                bosstock.save()
            else:
                for st in buy_stock:
                    # 卖出股票>买入股票
                    if amount >= st.amount:
                        # 卖出股票-买入股
                        amount = amount - st.amount
                        # 持仓冻结更改
                        hold[0].amount = hold[0].amount - st.amount
                        hold[0].frozen = hold[0].frozen - st.amount
                        hold.save()
                        fund[0].money = fund[0].money + st.amount*st.price
                        fund.save()
                        buser = Hold.objects.filter(user=st.user,stock=stock)
                        if len(buser)>0:
                            buser = Hold.objects.filter(user=st.user,stock=stock).update(amount=F('amount')+st.amount)
                        else:
                            buser = Hold.objects.create(user=st.user,stock=stock,amount=st.amount,frozen=0)
                        dealstock = DealStock.objects.create(suser=user, buser=st.user, price=st.price,amount=st.amount, datetime=datetimes, stock=stockdetail)
                        st.delete()
                    else:
                        st.amount = st.amount - amount
                        st.save()
                        hold[0].amount = hold[0].amount - amount
                        hold[0].frozen = hold[0].frozen - amount
                        hold.save()
                        fund[0].money = fund[0].money + amount * st.price
                        fund.save()
                        buser = Hold.objects.filter(user=st.user, stock=stock)
                        if len(buser) > 0:
                            buser = Hold.objects.filter(user=st.user, stock=stock).update(amount=F('amount') + amount)
                        else:
                            buser = Hold.objects.create(user=st.user, stock=stock, amount=amount, frozen=0)
                        dealstock = DealStock.objects.create(suser=user, buser=st.user, price=st.price,amount=amount, datetime=datetimes,stock=stockdetail)
                if amount > 0:
                    bosstock = BOSStock()
                    bosstock.user = user
                    bosstock.stock = stock
                    bosstock.role = 1
                    bosstock.price = price
                    bosstock.amount = amount
                    bosstock.datetime = datetimes
                    bosstock.save()
                elif amount < 0:
                    return HttpResponse(json.dumps({"result": True, "data": "剩余股票已挂单", "error": ""}))
        else:
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "所持股票数量不足"}))
    elif sob == "buy":
        fund = Fund.objects.filter(user_id=user.id)
        money = fund[0].money - amount * price
        stock = Stock.objects.get(number=stockNo)
        stockdetail = json.dumps(stock)
        datetimes = datetime.datetime.now()
        if money > 0:
            # 交易/冻结
            fund[0].frozen_money = fund[0].frozen_money + amount * price
            fund.save()
            sale_stock = BOSStock.objects.filter(stock__number=stockNo, role=1,
                                                 price__range=(price + price_range, price))
            if len(sale_stock) < 0:
                # 挂单
                bosstock = BOSStock()
                bosstock.user = user
                bosstock.stock = stock
                bosstock.role = 0
                bosstock.price = price
                bosstock.amount = amount
                bosstock.datetime = datetimes
                bosstock.save()
            else:
                # 交易
                for st in sale_stock:
                    # 买入股票 > 卖出股票
                    if amount > st.amount:
                        hold = Hold.objects.filter(user_id=user.id, stock=stock)
                        if len(hold) > 0:
                            hold[0].amount = hold[0].amount + st.amount
                            hold.save()
                        else:
                            Hold.objects.create(user_id=user.id, stock=stock, amount=st.amount, frozen=0)
                        bfund = Fund.objects.filter(user_id=user.id)
                        bfund[0].money = bfund[0].money - st.amount * st.price
                        bfund[0].frozen_money = bfund[0].frozen_money - st.amount * st.price
                        bfund.save()
                        sfund = Fund.objects.filter(user=st.user)
                        sfund[0].money = sfund[0].money + st.amount * st.price
                        sfund.save()
                        Hold.objects.filter(user=st.user, stock=stock).update(amount=F('amount') - st.amount,
                                                                              frozen=F('frozen') - st.amount)
                        dealstock = DealStock.objects.create(suser=user, buser=st.user, price=st.price,
                                                             amount=st.amount, datetime=datetimes, stock=stockdetail)
                        amount = amount - st.amount
                        st.delete()
                    else:
                        # 买入股票 < 卖出股票
                        hold = Hold.objects.filter(user=user, stock=stock)
                        if len(hold) > 0:
                            hold[0].amount = hold[0].amount + amount
                            hold.save()
                        else:
                            Hold.objects.create(user=user, stock=stock, amount=amount, frozen=0)
                        bfund = Fund.objects.filter(user=user)
                        bfund[0].frozen_money = bfund[0].frozen_money - amount * price
                        bfund[0].money = bfund[0].money - amount * price
                        bfund.save()
                        Hold.objects.filter(user=st.user).update(amount=F('amount') - amount)
                        sfund = Fund.objects.filter(user=st.user)
                        sfund[0].money = sfund[0].money + amount * price
                        sfund.save()
                        st.amount = st.amount - amount
                        # 挂单
                        st.save()
                if amount > 0:
                    bosstock = BOSStock()
                    bosstock.user = user
                    bosstock.stock = stock
                    bosstock.role = 0
                    bosstock.price = price
                    bosstock.amount = amount
                    bosstock.datetime = datetimes
                    bosstock.save()
                elif amount < 0:
                    return HttpResponse(json.dumps({"result": True, "data": "剩余股票已挂单", "error": ""}))
        else:
            # 充值
            charge()

def charge(user, remoney):
    pass















