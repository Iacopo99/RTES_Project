import random
import threading
from threading import Thread
from priority.PrioPolicy import PrioPolicy


def proc(p_fq):
    i = 0
    pr = random.randint(0, 4)
    while i in range(3):
        var = random.randint(0, 1)
        n = threading.get_native_id()
        if var:
            print('thread {} trying to do a push with priority {}'.format(n, pr))
            p_fq.push(n, n, pr)
            print('push {} done'.format(n))
        else:
            print('thread {} trying to reading the data'.format(n))
            ris = p_fq.get_length(n)
            print('length get by the thread {} : {}'.format(n, ris))
        i += 1


if __name__ == '__main__':
    t = []
    pp = PrioPolicy()
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
