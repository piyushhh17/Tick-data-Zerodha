import logging
from kiteconnect import KiteTicker
import time
import pandas as pd
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

redis_client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

logging.basicConfig(level=logging.DEBUG)

# Initialise
kws = KiteTicker("j2offcolhvyskf8r", "GXOdTC4l6kV6mikGkoLbZcsoIxBZ90MX")
tokens = [256265, 260105]
stock_names = {256265:'NIFTY 50', 260105:'NIFTY BANK'}
dicto = {}
def on_ticks(ws, ticks):
    global high, low, minute, count
    global dicto, listo, entry_flag
    
    for tick in ticks:
        if tick['instrument_token'] == 256265:
            datetime_str = tick['exchange_timestamp'].strftime("%d-%m-%y %H:%M:%S")
            current_time = datetime.now()
            current_time = current_time.strftime("%d-%m-%y %H:%M:%S")
            time_format = "%d-%m-%y %H:%M:%S"
            datetime_str = datetime.strptime(datetime_str, time_format)
            datetime_str = datetime_str - timedelta(minutes=1)
            current_time = datetime.strptime(current_time, time_format)
            ltp = tick['last_price']
            datetime_str = datetime_str.strftime("%d-%m-%y %H:%M:%S")
            dicto['time'] = datetime_str
            dicto['ltp'] = ltp
            print (dicto)
            redis_key = 'NIFTY 50'
            redis_client.hmset(redis_key, dicto)

        elif tick['instrument_token'] == 260105:
            datetime_str = tick['exchange_timestamp'].strftime("%d-%m-%y %H:%M:%S")
            current_time = datetime.now()
            current_time = current_time.strftime("%d-%m-%y %H:%M:%S")
            time_format = "%d-%m-%y %H:%M:%S"
            datetime_str = datetime.strptime(datetime_str, time_format)
            datetime_str = datetime_str - timedelta(minutes=1)
            current_time = datetime.strptime(current_time, time_format)
            ltp = tick['last_price']
            datetime_str = datetime_str.strftime("%d-%m-%y %H:%M:%S")
            dicto['time'] = datetime_str
            dicto['ltp'] = ltp
            print (dicto)
            redis_key = 'NIFTY BANK'
            redis_client.hmset(redis_key, dicto)




def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe(tokens)

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, tokens)
    

def on_close(ws, code, reason):
    # elapsed_time = time.time() - start_time
    # On connection close stop the event loop.
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

    # ws.stop()

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.

kws.connect()
