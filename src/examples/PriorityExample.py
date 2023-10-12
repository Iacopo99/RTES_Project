import random
import threading
from threading import Thread
from priority.PrioPolicy import PrioPolicy


def proc(p_fq):
    i = 0
    pr = random.randint(2, 10)
    while i in range(3):
        var = random.randint(0, 4)
        n = threading.get_native_id()
        if not var:
            print('thread {} trying to do a pop with priority {}'.format(n, pr))
            ris = p_fq.pop(n, pr)
            print('pop {} done: {}'.format(n, ris))
        elif var == 1:
            print('thread {} trying to do a push with priority {}'.format(n, pr))
            p_fq.push(n, n, pr)
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
        i += 1


if __name__ == '__main__':
    t = []
    pp = PrioPolicy('head', 2, 10)
    for i in range(15):
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
