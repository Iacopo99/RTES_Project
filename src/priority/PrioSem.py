from threading import Semaphore
from generals.ImplementSem import ImplementSem


class PrioSem(ImplementSem):

    __nbw_p = []
    def_prio = 0

    def __init__(self, lower_bound=0, upper_bound=4):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        for i in range(lower_bound, upper_bound + 1):
            self.__nbw_p.append(0)
        self.def_prio = round((lower_bound + upper_bound) / 2)

    def checking_prio(self, prio):
        if (prio < self.lower_bound) | (prio > self.upper_bound):
            raise ValueError(
                'prio variable must be an integer between {} (higher) an {} (lower)'.format(self.lower_bound,
                                                                                            self.upper_bound))

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

    def free_writer(self):
        self.nbw -= 1
        self.nw += 1
        t_p = -1
        for i in range(self.lower_bound, self.upper_bound + 1):
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
