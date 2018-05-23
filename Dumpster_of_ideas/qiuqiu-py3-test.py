
'''
just another script for 欢乐球球. it seems that the score is contained in a request query,
but I failed to alter it and feels lonely after trying that non-sense. just throw it away.
'''

import json
from mitmproxy import ctx
from pprint import pformat


def response(flow):
    path = flow.request.path
    if 'p/ip:10.20.3.31:2307' in path:
        ctx.log.info('Start')
        query = flow.request.query
        # ctx.log.info(pformat(query))
        '''
        if '"body"' in str(query):
            ctx.log.info('have body')
        '''
        query.set_all('"2":13', '"2":50')
        ctx.log.info(pformat(query))
        # flow.request.replace('"2":23', '"2":500')
        '''
        if type(query) is dict:
            ctx.log.info('true')
        
        if type(data) is dict:
            for k1, v1 in data.items():
                if k1 == '_t':
                    ctx.log.debug('v1 = ' + v1)

                if k1 == 'cmd':
                    for k2, v2 in v1.items():
                        if k2 == 'body':
                            v2['2'].update({'2': 800, 'num1': ' 对 ', 'num2': ' 对 ', 'symbol': ' 对 '})
                        else:
                            v.update({'seconds': 20, 'num1': ' 错 ', 'num2': ' 错 ', 'symbol': ' 错 '})
                '''

        # flow.request.query = query
        return
