import csv
import time
import traceback

import pandas
from ib_insync import *
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import traceback
from copy import deepcopy

from kiteconnect import KiteConnect

from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
warnings.filterwarnings('ignore')
import math
import redis
import six
import sys
import time
import json
import struct
import logging
import threading
from datetime import datetime, timedelta
from twisted.internet import reactor, ssl
from twisted.python import log as twisted_log
from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory, connectWS


# from .__version__ import __version__, __title__
def generateAccess():
    global access_token, key_secret, kite, instrument_df, tickers, quantity
    access_token = 'GXOdTC4l6kV6mikGkoLbZcsoIxBZ90MX'
    key_secret = 'j2offcolhvyskf8r'
    kite = KiteConnect(api_key=key_secret)
    kite.set_access_token(access_token)
def instrumentLookup(symbol):
    global access_token, key_secret, kite, instrument_df, tickers, quantity
    try:
        return instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0]
    except:
        return -1


def getInstruments():
    global access_token, key_secret, kite, instrument_df, tickers, quantity
    while True:
        try:
            instrument_dump = kite.instruments()
            instrument_df = pd.DataFrame(instrument_dump)
            break
        except Exception as e:
            print(str(e))
            continue
from kiteconnect import KiteConnect
generateAccess()
getInstruments()
def get_atm_nifty(ltp):
    nifty_step_size = 50
    mod = math.fmod(ltp, nifty_step_size)
    if mod >= 25:
        atm_value = ltp - mod + nifty_step_size
    else:
        atm_value = ltp - mod
    #print('Nifty ATM Value: ', int(atm_value))
    return int(atm_value)

def get_atm_bank_nifty(ltp):
    bnf_step_size = 100
    mod = math.fmod(ltp, bnf_step_size)
    if mod > 50:
        atm_value = int((ltp//100)*100)+100
    else:
        atm_value = int(ltp//100)*100
    return atm_value
    

def fetch_ltp(kite, name):
    '''
    Function takes kite object, name of exchange and name of instruments
    and returns the ltp
    '''
    instrument_name = str(instrumentLookup(name))
    
    ltp = kite.ltp(instrument_name)[instrument_name]['last_price']
    return ltp
def month00():
    today = datetime.now().strftime("%Y-%m-%d")
    months_representation = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
    time_format = "%Y-%m-%d"
    today = datetime.strptime(today, time_format)
    year = str(today.year)
    # print(year[-2:])
    return (year[-2:] + months_representation[today.month])

def month01():
    today = datetime.now().strftime("%Y-%m-%d")
    months_representation = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
    time_format = "%Y-%m-%d"
    today = datetime.strptime(today, time_format)
    year = str(today.year)
    # print(year[-2:])
    return (year[-2:] + months_representation[(today.month+1)%12])

def week00_nf():    
    all_expiry_dates = [str(x) for x in sorted(list(set(instrument_df[(instrument_df['exchange'] == 'NFO') & (instrument_df['name'] == 'NIFTY')]['expiry'].values)))]
    x = all_expiry_dates[0]
    y = all_expiry_dates[1]
    if y[5:7] != x[5:7]:
        return month00()
    week = x[-2:]
    year = x[2:4]
    today = datetime.now().strftime("%Y-%m-%d")
    time_format = "%Y-%m-%d"
    today = datetime.strptime(today, time_format)
    month = today.month
    month = str(month)
    if month == '10':
        month = 'O'
    if month == '11':
        month = 'N'
    if month == '12':
        month = 'D'
    return (str(year)+month+str(week))
# print(all_expiry_dates[0][-2:])

def week01_nf():    
    all_expiry_dates = [str(x) for x in sorted(list(set(instrument_df[(instrument_df['exchange'] == 'NFO') & (instrument_df['name'] == 'NIFTY')]['expiry'].values)))]
    x = all_expiry_dates[1]
    y = all_expiry_dates[2]
    if y[5:7] != x[5:7]:
        return month00()
    week = x[-2:]
    year = x[2:4]
    today = datetime.now().strftime("%Y-%m-%d")
    time_format = "%Y-%m-%d"
    today = datetime.strptime(today, time_format)
    month = today.month
    month = str(month)
    if month == '10':
        month = 'O'
    if month == '11':
        month = 'N'
    if month == '12':
        month = 'D'
    return (str(year)+month+str(week))
def week00_bn():    
    all_expiry_dates = [str(x) for x in sorted(list(set(instrument_df[(instrument_df['exchange'] == 'NFO') & (instrument_df['name'] == 'BANKNIFTY')]['expiry'].values)))]
    x = all_expiry_dates[0]
    y = all_expiry_dates[1]
    if y[5:7] != x[5:7]:
        return month00()
    week = x[-2:]
    year = x[2:4]
    today = datetime.now().strftime("%Y-%m-%d")
    time_format = "%Y-%m-%d"
    today = datetime.strptime(today, time_format)
    month = today.month
    month = str(month)
    if month == '10':
        month = 'O'
    if month == '11':
        month = 'N'
    if month == '12':
        month = 'D'
    return (str(year)+month+str(week))
# print(all_expiry_dates[0][-2:])

def week01_bn():    
    all_expiry_dates = [str(x) for x in sorted(list(set(instrument_df[(instrument_df['exchange'] == 'NFO') & (instrument_df['name'] == 'BANKNIFTY')]['expiry'].values)))]
    x = all_expiry_dates[1]
    y = all_expiry_dates[2]
    if y[5:7] != x[5:7]:
        return month00()
    week = x[-2:]
    year = x[2:4]
    today = datetime.now().strftime("%Y-%m-%d")
    time_format = "%Y-%m-%d"
    today = datetime.strptime(today, time_format)
    month = today.month
    month = str(month)
    if month == '10':
        month = 'O'
    if month == '11':
        month = 'N'
    if month == '12':
        month = 'D'
    return (str(year)+month+str(week))
# print(all_expiry_dates[0][-2:])

#ITM CE
#50 below ATM
# ltp_data = kite.ltp("256265")
# ltp = ltp_data["256265"]['last_price']
listo = []
def ITM_ce_nf():
    global token_list
    atm_ce_nf = int(get_atm_nifty(fetch_ltp(kite, 'NIFTY 50')))-500
    # print(atm_ce_nf)
    for i in range(1, 10):
        itm_ce = atm_ce_nf + (50*i)
        listo.append(itm_ce)
        exchange = "NFO"
        tradingsymbol = "NIFTY" + week00_nf() + str(itm_ce) + "CE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "NIFTY" + week01_nf() + str(itm_ce) + "CE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "NIFTY" + month00() + str(itm_ce) + "CE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "NIFTY" + month01() + str(itm_ce) + "CE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))

def ITM_pe_nf():
    global token_list
    atm_ce_nf = int(get_atm_nifty(fetch_ltp(kite, 'NIFTY 50')))-500
    # print(atm_ce_nf)
    for i in range(1, 10):
        itm_ce = atm_ce_nf + (50*i)
        listo.append(itm_ce)
        exchange = "NFO"
        tradingsymbol = "NIFTY" + week00_nf() + str(itm_ce) + "PE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "NIFTY" + week01_nf() + str(itm_ce) + "PE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "NIFTY" + month00() + str(itm_ce) + "PE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "NIFTY" + month01() + str(itm_ce) + "PE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))

def ITM_ce_bn():
    global token_list
    atm_ce_bn = int(get_atm_nifty(fetch_ltp(kite, 'NIFTY BANK')))-1000
    # print(atm_ce_bn)
    for i in range(1, 10):
        itm_ce = atm_ce_bn + (100*i)
        listo.append(itm_ce)
        exchange = "NFO"
        tradingsymbol = "BANKNIFTY" + week00_bn() + str(itm_ce) + "CE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "BANKNIFTY" + week01_bn() + str(itm_ce) + "CE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "BANKNIFTY" + month00() + str(itm_ce) + "CE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "BANKNIFTY" + month01() + str(itm_ce) + "CE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
            
def ITM_pe_bn():
    global token_list
    atm_ce_bn = int(get_atm_nifty(fetch_ltp(kite, 'NIFTY BANK')))-1000
    # print(atm_ce_bn)
    for i in range(1, 10):
        itm_ce = atm_ce_bn + (100*i)
        listo.append(itm_ce)
        exchange = "NFO"
        tradingsymbol = "BANKNIFTY" + week00_bn() + str(itm_ce) + "PE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "BANKNIFTY" + week01_bn() + str(itm_ce) + "PE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "BANKNIFTY" + month00() + str(itm_ce) + "PE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
        tradingsymbol = "BANKNIFTY" + month01() + str(itm_ce) + "PE" 
        try:
            instrument_token_ce_nf=instrumentLookup(tradingsymbol)
            token_list.append(instrument_token_ce_nf)
        except Exception as e:
            print("Error:", str(e))
      
token_list = []
ITM_pe_nf()
ITM_ce_nf()
ITM_pe_bn()
ITM_ce_bn()
print(len(token_list))

