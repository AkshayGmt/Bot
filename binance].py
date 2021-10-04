# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 11:35:56 2021

@author: Lenovo
"""

from binance import Client
import pandas as pd
#%run ./Binance_keys.ipynb

api_key = "jlWmXAyvJYX1jZtDu9OO0BtvxbgH0bfCArJVnvlu6rqWEOEoY5hyzD7qkWfmEjoI" 
api_secret = "TykTlfC5eUJlhJVt5V9ufNaI9CQznt2cw0X4LESbKuU1NkfFNznECQBHWAx7inOv"
client = Client(api_key,api_secret)
client.get_account()
# Account Imformation

#datastream via websocket -will not be covered in this one

pd.DataFrame(client.get_historical_klines('BTCUSDT','1m', '30m ago UTC'))

def getminutedata(symbol, interval,lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback + 'min ago UTC'))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time','Open','High','Low','Close','Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame




getminutedata('BTCUSDT', 'm', '30')
test = getminutedata('BTCUSDT', '1m', '30')
#test.Open.plot() 
print(test)
#buy if asset fell by more then 0.2% within the last 30 min 
#sell if asset rises by more than 0.15% or falls further by 0.15%

def strategytest(symbol,qty, entried=False):
    df = getminutedata(symbol,'1m', '30m')
    cumulret = (df.Open.pct_change() +1 ).cumprod()-1
    if not entried:
        if cumulret[-1] < -0.002:
            order = client.create_order(symbol=symbol,side='BUY',type='Market',quantity='qty')
            print(order)
            entried =True
        else:
            print("No trade has been executed")
    if entried:
        while True:
            df = getminutedata(symbol, '1m', '30')
            sincebuy = df.loc[df.index > pd.to_datatime(order['transactTime'], unit ='ms')]
            if len (sincebuy) > 0:
                sincebuyret = (sincebuy.Open.pct_change() +1) .cumprod()-1
                
                if sincebuyret[-1]> 0.0015 or sincebuyret[-1]<0.0015:
                    order = client.create_order(symbol=symbol,side='SELL',type='MARKET',quantity=qty)
                    print(order)
                    break
             
strategytest('BTCUSDT', 0.0001)                
                
              
                
