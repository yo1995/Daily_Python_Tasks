# coding: utf-8

from multiprocessing import Pool
import time


def task(msg):
    print('hello, %s' % msg)
    time.sleep(1)
    return 'msg: %s' % msg


if __name__ == '__main__':
    pool = Pool(processes=4)

    msgs = [x for x in range(10)]
    print(msgs)
    results = pool.map_async(task, msgs).get(6)

    pool.close()
    pool.join()

    print('processes done, result:')

    for x in results:
        print(x)
