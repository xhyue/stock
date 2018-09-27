#!/usr/bin/env python3
#coding=utf-8

import tushare as ts

def stock_A():
    df = ts.get_realtime_quotes('sh')
    return df


def stock_company(code):
    code = str(code)
    df = ts.get_realtime_quotes(code)
    return df


# 热点资讯
def stock_news():
    df = ts.guba_sina()
    return df


# 大盘指数行情
def stock_index():
    df = ts.get_index()
    return df


# 实时解盘
def stock_breakup():
    df = ts.get_latest_news()
    return df


# k线数据
def stock_k_data():
    df = ts.get_hist_data('sh')
    return df


# def stock_notices():
#     df = ts.get_notices()
#     return df