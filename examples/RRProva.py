import random
import threading
from threading import Thread
from rr.RRPolicy import RRPolicy


def proc(p_fq):
    for iter in range(3):
        var = random.randint(0, 1)
        n = threading.get_native_id()
        if var:
            print('thread {} trying to push'.format(n))
            p_fq.push(n, n)
            print('push {} done'.format(n))
        else:
            print('thread {} trying to read data'.format(n))
            ris = p_fq.get_length(n)
            print('length\'s queue get by the thread {} : {}'.format(n, ris))


if __name__ == '__main__':
    t = []
    pp = RRPolicy(q=0.3)
    for i in range(10):
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
