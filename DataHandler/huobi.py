# -*- coding: utf-8 -*-

from websocket import create_connection
import gzip
import time
import sys
import json
from market_snapshot import *


def HandleDict(d, f):
  shot = MarketSnapshot()
  if "ch" not in d:
    return
  shot.ticker = d['ch'].split('.')[1]
  shot.time = d['tick']['ts']/1000
  d = d['tick']
  for i in range(5):
    shot.bids[i] = d['bids'][i][0]
    shot.bid_sizes[i] = d['bids'][i][1]
    shot.asks[i] = d['asks'][i][0]
    shot.ask_sizes[i] = d['asks'][i][1]
  shot.last_trade = 100.0
  shot.open_interest = 100.0
  shot.ShowCSV(f)

if __name__ == '__main__':
  f = open('futures.csv', 'w')
  while(1):
    try:
      ws = create_connection("wss://www.hbdm.com/ws")
      print('connet address ok')
      break
    except Exception as e:
      print('connect ws error,retry...')
      print(e)
      time.sleep(5)
    # 订阅 KLine 数据
    
  tradeStr_kline="""
  {"sub": "market.BTC_CQ.kline.1min",  "id": "id1"}
  """

  # 订阅 Market Detail 数据
  tradeStr_marketDetail="""
  {"sub": "market.BTC_CQ.detail",  "id": "id6" }
  """

  # 订阅 Trade Detail 数据
  tradeStr_tradeDetail="""
  {"sub": "market.BTC_CQ.trade.detail", "id": "id7"}
  """

  # 请求 KLine 数据
  tradeStr_klinereq="""
  {"req": "market.BTC_CQ.kline.1min", "id": "id4"}
  """

  # 请求 Trade Detail 数据
  tradeStr_tradeDetail_req="""
  {"req": "market.BTC_CQ.trade.detail", "id": "id5"}
  """

  # 订阅 Market Depth 数据
  tradeStr_marketDepth="""{ "sub": "market.BTC_CQ.depth.step0", "id": "id9"}"""

  tradeStr_marketDepth2="""
  {
      "sub": "market.XRP_CQ.depth.step0", "id": "id9"
  }
  """
  coin_list = ["BTC", "ETC", "ETH", "EOS", "LTC", "BCH", "XRP", "TRX", "BSV"]
  due_list = ["CW", "NW", "CQ"]
  sub_list = []
  count = 0
  for c in coin_list:
    for d in due_list:
      ws.send("""{ "sub": "market.%s_%s.depth.step0", "id": "id%d"}""" % (c, d, count))
      count += 1
  #ws.send(tradeStr_marketDepth)
  #ws.send(tradeStr_marketDepth2)
  trade_id = ''
  while(1):
    compressData=ws.recv()
    result=gzip.decompress(compressData).decode('utf-8')
    if result[:7] == '{"ping"':
      ts=result[8:21]
      pong='{"pong":'+ts+'}'
      ws.send(pong)
      #ws.send(tradeStr_kline)
      print('meeting ping')
    else:
      try:
        if trade_id == result['data']['id']:
          print('重复的id')
          break
        else:
          trade_id = result['data']['id']
      except Exception:
        pass
      a = json.loads(result)
      HandleDict(a, f)
