from threading import Semaphore
from generals.ImplementSem import ImplementSem


class PrioSem(ImplementSem):
    __lower_bound = 0
    __upper_bound = 4
    def_prio = round((__lower_bound + __upper_bound) / 2)

    __nbw_p = []
    for i in range(__lower_bound, __upper_bound + 1):
        __nbw_p.append(0)

    def __init__(self, prio_type=1):
        if (prio_type == 'DYNAMIC') | (prio_type == 'STATIC') | (prio_type == 1) | (prio_type == 0):
            if (prio_type == 'DYNAMIC') | (prio_type == 1):
                self.prio_type = 1
            else:
                self.prio_type = 0
        else:
            raise ValueError(
                'prio_type variable must be an integer between 0 and 1 (default) or a string between \'DYNAMIC\' and \'STATIC\'')

    def checking_prio(self, prio):
        if (prio < self.__lower_bound) | (prio > self.__upper_bound):
            raise ValueError(
                'prio variable must be an integer between {} (higher) an {} (lower)'.format(self.__lower_bound,
                                                                                            self.__upper_bound))

    def before_writing(self, i=-1, prio=def_prio):
        s_w = Semaphore(value=0)
        self.checking_prio(prio)

        self.mtx.acquire()
        if (self.nr > 0) | (self.nw > 0):
            self.nbw += 1
            self.__nbw_p[prio] += 1
            c = self.__nbw_p[prio]
            if i != -1:
                print('thread writer {} BLOCKED'.format(i))
            self.private_w[(c, prio)] = s_w
        else:
            self.nw += 1
            s_w.release()
        self.mtx.release()
        s_w.acquire()

    def after_writing(self):
        self.mtx.acquire()
        self.nw -= 1
        if self.nbr > 0:
            while self.nbr > 0:
                self.nbr -= 1
                self.nr += 1
                s_r = self.private_r.pop(1)
                s_r.release()
                new = {}
                for i in self.private_r.keys():
                    new[i - 1] = self.private_r[i]
                self.private_r = new
        elif self.nbw > 0:
            self.__free_writer()
        self.mtx.release()

    def __free_writer(self):
        self.nbw -= 1
        self.nw += 1
        t_p = -1
        for i in range(self.__lower_bound, self.__upper_bound + 1):
            if (1, i) in self.private_w:
                t_p = i
                s_w = self.private_w.pop((1, i))
                s_w.release()
                self.__nbw_p[i] -= 1
                break
        new = {}
        for i in list(self.private_w.keys()):
            if i[1] == t_p:
                new[(i[0] - 1, t_p)] = self.private_w[(i[0], t_p)]
            else:
                new[i] = self.private_w[i]
        self.private_w = new
