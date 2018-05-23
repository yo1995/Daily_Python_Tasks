import json
from mitmproxy import ctx
from pprint import pformat


def response(flow):
    path = flow.request.path
    if path == '/index/index_one_nine_six/sprint_game' or path == '/index/index_one_three_seven/make_question':
        ctx.log.info('Start')
        data = json.loads(flow.response.text)
        ctx.log.info(pformat(data))

        if type(data) is list:
            for m in data:
                if type(m) is dict:
                    m['seconds'] = 20
                    m['symbol'] = ' 对 ' if m['is_true'] == '1' else ' 错 '  # 直接将答题区运算符号改为答案
        '''
        既然是开挂，那就丧心病狂一点吧！
        if type(data) is dict:
            for k, v in data.items():
                if k.isdigit() and type(v) == dict:
                    v.update({'seconds': 20, 'symbol': ' 对 ' if v['is_true'] == 1 else ' 错 '})
        '''
        if type(data) is dict:
            for k, v in data.items():
                if k.isdigit() and type(v) == dict:
                    if v['is_true'] == 1:
                        v.update({'seconds': 20, 'num1': ' 对 ', 'num2': ' 对 ', 'symbol': ' 对 '})
                    else:
                        v.update({'seconds': 20, 'num1': ' 错 ', 'num2': ' 错 ', 'symbol': ' 错 '})

        flow.response.text = json.dumps(data)
        return
