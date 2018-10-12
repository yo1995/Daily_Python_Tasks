from multiprocessing import Manager, Pool, Lock
import time


def test(d, l):
    l.acquire()
    d['a'] += 1
    d['b'] += 1
    l.release()


def multi():
    with Manager() as manager:
        dct = manager.dict({'a': 0, 'b': 0})
        pool = Pool()
        l = manager.Lock()
        for i in range(5000):
            pool.apply_async(test, args=(dct, l, ))
            print(i)

        pool.close()
        pool.join()

        return dict(dct)


def single():
    dct = dict({'a': 0, 'b': 0})
    for i in range(5000):
        dct['a'] += 1
        dct['b'] += 1

    return dict(dct)


if __name__ == '__main__':
    t1 = time.time()
    a = multi()
    print('mp time used: ' + str(time.time() - t1))
    print('result is: ', a)

    t2 = time.time()
    b = single()
    print('single time used: ' + str(time.time() - t2))
    print('result is: ', b)


