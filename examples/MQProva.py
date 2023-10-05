import random
import threading
from threading import Thread
import time
from gqueues.MQPolicy import MQPolicy


def proc(p_fq):
    n = threading.get_native_id()
    time.sleep(float(random.randint(0, 1000) / 1000))
    for iter in range(3):
        var = random.randint(0, 1)
        if var:
            print('thread {} trying to push'.format(n))
            p_fq.push(n, n)
            print('push {} done'.format(n))
        else:
            print('thread {} trying to read data'.format(n))
            ris = p_fq.get_length(n)
            print('length\'s queue get by the thread {} : {}'.format(n, ris))
    print('thread {} COMPLETED'.format(n))


if __name__ == '__main__':
    t = []
    q = [10]
    pp = MQPolicy(q)
    for i in range(5):
        pt = Thread(target=proc, args=[pp])
        t.append(pt)
    for i in t:
        try:
            i.start()
        except Exception:
            print('thread {} does not start'.format(i))
    for i in t:
        i.join()
    print(pp)
