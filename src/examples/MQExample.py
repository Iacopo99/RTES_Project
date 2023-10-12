import random
import threading
from threading import Thread
import time
from multiple_queues.MQPolicy import MQPolicy


def proc(p_fq):
    n = threading.get_native_id()
    time.sleep(float(random.randint(0, 1000) / 1000))
    for iter in range(3):
        var = random.randint(0, 4)
        if not var:
            print('thread {} trying to do a pop'.format(n))
            ris = p_fq.pop(n)
            print('pop {} done: {}'.format(n, ris))
        elif var == 1:
            print('thread {} trying to do a push'.format(n))
            p_fq.push(n, n)
            print('push {} done'.format(n))
        elif var == 2:
            print('thread {} trying to reading the data'.format(n))
            ris = p_fq.get_length(n)
            print('length get by the thread {} : {}'.format(n, ris))
        elif var == 3:
            print('thread {} calls empty method'.format(n))
            ris = p_fq.empty(n)
            print('empty from thread {}: {}'.format(n, ris))
        elif var == 4:
            print('thread {} trying to get the head'.format(n))
            ris = p_fq.get_head(n)
            print('head get by thread {}: {}'.format(n, ris))
    print('thread {} COMPLETED'.format(n))


if __name__ == '__main__':
    t = []
    q = [0.1, 0.2, 0.5]
    pp = MQPolicy(q)
    for i in range(20):
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
