import json
from mitmproxy import ctx
from pprint import pformat


def response(flow):
    path = flow.request.path
    if path == '/index/index_one_nine_five/make_question' or path == '/index/index_one_three_six/make_question':
        ctx.log.info('Start')
        data = json.loads(flow.response.text)
        ctx.log.info(pformat(data))

        if type(data) is list:
            for m in data:
                if type(m) is dict:
                    m['seconds'] = 20
                    m['symbol'] = ' 对 ' if m['is_true'] == '1' else ' 错 '  # 直接将答题区运算符号改为答案

        if type(data) is dict:
            for k, v in data.items():
                if type(v) == dict:
                    v.update({'seconds': 20, 'symbol': ' 对 ' if v['is_true'] == 1 else ' 错 '})

        flow.response.text = json.dumps(data)
        return
