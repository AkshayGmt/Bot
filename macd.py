# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 21:50:53 2021

@author: Lenovo
"""


def strategy(symbol, qty, open_position = False):
    while True:
        frame = getminutedata('BTCUSDT','1m','30m UTC')
        if not open_position:
            if ta.trend.macd_diff(frame.Close).iloc[-1] > 0\
            and ta.trend.macd_diff(frame.Close).iloc[-2] <0:
                order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quantity=qty)
                print(order)
                open_position = True
                buyprice = float(order['fills'][0]['price'])
                break
        if open_position:
            while True:
                frame = getminutedata(symbol)
                if ta.trend.macd_diff(frame.Close).iloc[-1]<0 \
                and ta.trend.macd_diff(frame.Close).iloc[-2] >0:
                    order=client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=qty)
                    print(order)
                    sellprice = float(order['fills'][0]['price'])
                    print(f'profit = {(sellprice-buyprice)/buyprice}')
                    open_position = False
                    break