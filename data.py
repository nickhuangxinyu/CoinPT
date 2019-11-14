import json
import websocket # pip install websocket-client

from configparser import ConfigParser

import logzero # pip install logzero
import logging

def on_error(ws,error):
    print(error)

def on_close(ws):
    ws.close()
    print("on close....")
    ws.run_forever()
    print("websocket closed")

def on_message(ws, message):
    # {'stream': 'eosbtc@depth5', 'data': {'lastUpdateId': 463816198, 'bids': [['0.00039270', '348.95000000'], ['0.00039260', '60.43000000'], ['0.00039250', '153.91000000'], ['0.00039240', '2055.12000000'], ['0.00039230', '509.14000000']], 'asks': [['0.00039290', '222.96000000'], ['0.00039300', '884.52000000'], ['0.00039310', '1943.47000000'], ['0.00039320', '490.16000000'], ['0.00039330', '57.52000000']]}}
    # symbol = json_message["stream"].split('@', 1)[0]
    json_message = json.loads(message)
    # print(json_message)
    logzero.logger.info(json_message)


if __name__ == '__main__':

    cfg = ConfigParser()
    cfg.read('config.ini')

    data_storage_path = cfg['data']['data_storage_path'] + "/data.log"
    # backupCount：最多产生多少个文件，maxBytes 10M
    logzero.logfile(data_storage_path, maxBytes=1024*1024 * 10, backupCount=9999999, loglevel=logging.INFO)
    # Set a custom formatter
    formatter = logging.Formatter('%(asctime)-15s - %(levelname)s: %(message)s')
    logzero.formatter(formatter)
    symbols = cfg['data']['symbols'].split(',')
    depth = cfg['data']['depth']
    base_url = cfg['data']['base_url']
    first = True   
    for symbol in symbols:
        if first:
            first = False
        else:
            base_url += '/'
        base_url += (symbol + '@depth' + depth)
    # print(base_url)    
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(base_url,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    print("开始通过websocket获取数据....")
    ws.run_forever()