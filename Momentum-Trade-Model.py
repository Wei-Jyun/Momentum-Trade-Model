
import datetime as dt
import json
from tkinter import Y
import pandas as pd 
import numpy as np
import yfinance as yf
import math


# Benchmark = "^GSPC"

def MomentumAdvice(stock, Benchmark_stock, start_date, end_date, n1, n2, n3):
    # 建立數據資料集
    # today = dt.date.today().strftime("%Y-%m-%d")
    short_MA = 20
    Benchmark = Benchmark_stock
    stock.sort()
    tickers = stock[0:]
    tickers.insert(len(tickers), Benchmark)
    print(tickers)
    tickers.sort()

    data = yf.download(tickers=tickers, start=start_date, end=end_date)

    data.reset_index(inplace=True) 
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.iloc[0:,:len(tickers)+1]
    data_list = tickers[0:]

    data_list.insert(0, 'Date')
    data.set_axis(data_list, axis = 'columns', inplace=True)
    data = data.dropna(axis = 0,subset = stock , inplace = False)
    data.reset_index(inplace = True) 
    for i in range(len(stock)):
        data['Short_MA -' + stock[i]] = data[stock[i]].rolling(int(short_MA)).mean()
    data['weekday'] = data['Date'].dt.day_name()

    # 讀取標的報價資料及計算標的報價變動率
    # 建立初始資金額
    Initial_Wealth = 10000
    # 設定時間參數、建構項目欄位
    for i in range(len(stock)):
        for ticker in stock:
            data[(f"{n1} days return- " + ticker)] = 0.0 
            data[(f"{n2} days return- " + ticker)] = 0.0 
            data[(f"{n3} days return- " + ticker)] = 0.0 
            data[("total return- " + ticker)] = 0.0 


    # 初始化並建立動能計算欄位，迴圈計算動能
    data["Output"], data['Benchmark'] = "", 0

    for i in range(0, len(data['Date'])):  
        for ticker in stock:
            if n1 == 0:
                data[(f"{n1} days return- " + ticker)] = 0.0
            else:
                if i >= n1:  
                    data.loc[i, (f"{n1} days return- " + ticker)] = (data[ticker][i] - data[ticker][i - n1]) / (data[ticker][i - n1])

            if n2 == 0:
                data[(f"{n2} days return- " + ticker)] = 0.0
            else:
                if i >= n2:  
                    data.loc[i, (f"{n2} days return- " + ticker)] = (data[ticker][i] - data[ticker][i - n2]) / (data[ticker][i - n2])

            if n3 == 0:
                data[(f"{n3} days return- " + ticker)] = 0.0
            else:
                if i >= n3:  
                    data.loc[i, (f"{n3} days return- " + ticker)] = (data[ticker][i] - data[ticker][i - n3]) / (data[ticker][i - n3])

        for ticker in stock:
            data.loc[i, ("total return- " + ticker)] = (data[(f"{n1} days return- " + ticker)][i] + 
                                                        data[(f"{n2} days return- " + ticker)][i] + 
                                                        data[(f"{n3} days return- " + ticker)][i] )
    t_lenth = [n1, n2, n3]
    data = data.iloc[max(t_lenth)+1:,0:]
    data = data.reset_index(drop=True)
    data.loc[0, 'Benchmark'] = Initial_Wealth / (data[Benchmark][0]) * data[Benchmark][0]

    # 抽出數據，用於獨立判斷投資建議
    for i in range(1, len(data['Date'])): 
        data.loc[i, 'Benchmark'] = Initial_Wealth / (data[Benchmark][0]) * (data[Benchmark][i])

    advice_frame = data['Date'].to_frame()

    for ticker in stock:
        advice_frame["total return- " + ticker] = data[("total return- " + ticker)]
    advice_frame_list = stock[0:]
    advice_frame_list.insert(0, "Date")   
    advice_frame.set_axis(advice_frame_list, axis = 'columns', inplace=True)
    advice_frame['Invest Advice'] = (advice_frame.iloc[0: ,1:]).idxmax(axis = 1)
    advice_frame = advice_frame.sort_values("Date", ascending = False)


    data = pd.merge(data, advice_frame[['Date', 'Invest Advice']], how = "left", on = 'Date')

    data['Output'] = data['Invest Advice']


    data = data.dropna(axis = 0,subset = ['Output'] , inplace = False)
    data.reset_index(inplace=True) 
    # 結束投資建議功能

    # 建立買進訊號欄位
    bs_columns = ["Buy Amount", "Sell Amount", "P/L", "Cash Account"]
    buy_signals = data
    for ticker in stock:
        buy_signals = buy_signals.drop(buy_signals[buy_signals.weekday != 'Friday'].index).reset_index(drop=True)
        bs_columns.insert(0, ticker + " Sell Amount")
        bs_columns.insert(0, ticker + " Buy Amount")
        bs_columns.insert(0, "Qty " + ticker)

    for bs_column in bs_columns: buy_signals[bs_column] = 0.0

    for ticker in stock:
        if buy_signals["Output"][0] == ticker:
            buy_signals.loc[0, "Qty " + ticker] = math.floor(Initial_Wealth / buy_signals[ticker][0])
            buy_signals.loc[0, ticker + " Buy Amount"] = buy_signals["Qty " + ticker][0] * buy_signals[ticker][0]

    for ticker in stock:
        buy_signals.loc[0, "Buy Amount"] += buy_signals[ticker + " Buy Amount"][0]

    buy_signals.loc[0, "Cash Account"] = Initial_Wealth - buy_signals["Buy Amount"][0]

    # 計算損益、回測紀錄
    for i in range(1, len(buy_signals["Output"])):
        # sell amount for VUSTX
        for ticker in stock:
            if buy_signals["Output"][i - 1] == ticker:
                buy_signals.loc[i, ticker + " Sell Amount"] = buy_signals["Qty " + ticker][i - 1] * buy_signals[ticker][i]
        # total sell amount
            buy_signals.loc[i, "Sell Amount"] += buy_signals[ticker + " Sell Amount"][i]
        
        for ticker in stock:
            if buy_signals["Output"][i] == ticker:
                buy_signals.loc[i, "Qty " + ticker] = math.floor((buy_signals["Cash Account"][i - 1] +
                                                            buy_signals["Sell Amount"][i]) / buy_signals[ticker][i])
                                                            
                buy_signals.loc[i, ticker + " Buy Amount"] = buy_signals["Qty " + ticker][i] * buy_signals[ticker][i]
        # total buy amount
        for ticker in stock:
            buy_signals.loc[i, "Buy Amount"] += buy_signals[ticker + " Buy Amount"][i]
        # cash account is the remaining balance after buying Whole shares
        buy_signals.loc[i, "Cash Account"] = buy_signals["Cash Account"][i - 1] - buy_signals["Buy Amount"][i] + buy_signals["Sell Amount"][i]
        # calculate profit and loss
        buy_signals.loc[i, "P/L"] = buy_signals["Sell Amount"][i] - buy_signals["Buy Amount"][i - 1]

    buy_signals["Port_val"] = Initial_Wealth

    for i in range(0, len(buy_signals["Port_val"])):
        if i == 0:
            buy_signals.loc[0, "Port_val"] = Initial_Wealth
        else:
            buy_signals.loc[i, "Port_val"] = buy_signals["Buy Amount"][i] + buy_signals["Cash Account"][i]


    # 夏普比率計算
    val_percent = buy_signals["Port_val"].pct_change()
    buy_signals['val_change'] = val_percent
    ratio = val_percent.mean() / val_percent.std()
    buy_signals["Sharpe"] = ratio
    buy_signals["std"] = val_percent.std()
    buy_signals["Port_percent"] = buy_signals["Port_val"] / Initial_Wealth

    result = {'Sharpe':buy_signals["Sharpe"][len(buy_signals["Port_val"])-1], 
            'std':buy_signals["std"][len(buy_signals["Port_val"])-1], 
            'porfit_percent':buy_signals["Port_percent"][len(buy_signals["Port_val"])-1]
            }

    buy_signals['Repeat'] = 0
    for i in range(1, len(buy_signals['Date'])):
        if buy_signals.loc[i, 'Output'] == buy_signals['Output'][i-1]:
            buy_signals.loc[i, 'Repeat'] = 1
        else:
            buy_signals.loc[i, 'Repeat'] = 0

    buy_signals = buy_signals.iloc[:,2:]

    # js = buy_signals[["Date", "Benchmark", "Invest Advice", "Port_val"]]

    js = buy_signals[["Date", "Port_val", "Output"]]
    js = js.rename(columns={'Port_val':'value' })
    js['Date'] = js['Date'].dt.strftime('%Y-%m-%d')


    # 提供日期資料
    js_date = js['Date']
    js_date = pd.concat([pd.Series(['Trade_Date']), js_date])
    js_date = js_date.to_json(orient='records')
    # 提供回測資產數據
    js_value = js['value']
    js_value = pd.concat([pd.Series(['Wealth_value']), js_value])
    js_value = js_value.to_json(orient='records')
    # 提供最新的投資訊號給前端
    last_invest_adivce = str(js.iloc[-1]['Output'])
    
    return js_date, js_value, last_invest_adivce

# 勝率計算-not yet push on the system
def Win_Fail(df, stockname):
    df = df.drop(df[df.Repeat == 1].index).reset_index(drop=True)
    df['SingeTradeProfit'] = 0

    for i in range(0, len(df['Date'])-1):
        df.loc[i, 'SingeTradeProfit'] = df["Port_val"][i+1] - df["Port_val"][i]

    WinTrade = df[(df["SingeTradeProfit"] > 0) & (df['Invest Advice'] == stockname)]
    FailTrade = df[(df["SingeTradeProfit"] <= 0) & (df['Invest Advice'] == stockname)]
    TotalMainTrade = df[(df['Invest Advice'] == stockname)]
    win_Percent = WinTrade['SingeTradeProfit'].count() / TotalMainTrade["SingeTradeProfit"].count()
    fail_Percent = FailTrade['SingeTradeProfit'].count() / TotalMainTrade["SingeTradeProfit"].count()
    print("Win Percent: ", win_Percent)
    print("Fail Percent: ", fail_Percent)
    return win_Percent, fail_Percent

