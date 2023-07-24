from threading import Semaphore
from Sem import Sem


class PrioSem(Sem):
    lower_bound = 0
    upper_bound = 4
    def_prio = round((lower_bound + upper_bound) / 2)

    nbr_p = nbw_p = []
    for i in range(lower_bound, upper_bound):
        nbr_p.append(0)
        nbw_p.append(0)

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
        if (prio < self.lower_bound) | (prio > self.upper_bound):
            raise ValueError(
                'prio variable must be an integer between {} (higher) an {} (lower)'.format(self.lower_bound,
                                                                                            self.upper_bound))

    def before_reading(self, i=-1, prio=def_prio):
        s_r = Semaphore(value=0)
        self.checking_prio(prio)

        self.mtx.acquire()
        if (self.nw > 0) | (self.nbw > 0):
            self.nbr += 1
            c = self.nbr
            if i != -1:
                print('thread reader {} BLOCKED'.format(i))
            self.private_r[c] = s_r
        else:
            self.nr += 1
            s_r.release()
        self.mtx.release()
        s_r.acquire()

    def after_reading(self):
        self.mtx.acquire()
        self.nr -= 1
        if (self.nbw > 0) & (self.nr == 0):
            self.free_writer()
        self.mtx.release()

    def before_writing(self, i=-1, prio=def_prio):
        s_w = Semaphore(value=0)
        self.checking_prio(prio)

        self.mtx.acquire()
        if (self.nr > 0) | (self.nw > 0):
            self.nbw += 1
            self.nbw_p[prio] += 1
            c = self.nbw_p[prio]
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
            for i in list(self.private_r.keys()):
                self.nbr -= 1
                self.nr += 1
                s_r = self.private_r.pop(1)
                s_r.release()
                new = {}
                for i in self.private_r.keys():
                    new[i - 1] = self.private_r[i]
                self.private_r = new
                """
                for i in range(self.lower_bound, self.upper_bound):
                    c = self.nbr_p[i]
                    for j in range(1, c):
                        if (j, i) in self.private_r:
                            t_p = i
                            s_r = self.private_r.pop((j, i))
                            s_r.release()
                            self.nbr_p[i] -= 1
                        else:
                            break
                new = {}
                for i in list(self.private_r.keys()):
                    if i[0] == t_p:
                        new[(i[0] - 1, t_p)] = self.private_r[(i[0], t_p)]
                    else:
                        new[i] = self.private_r[(i[0], t_p)]
                self.private_r = new"""
        elif self.nbw > 0:
            self.free_writer()
        self.mtx.release()

    def free_writer(self):
        self.nbw -= 1
        self.nw += 1
        t_p = -1
        for i in range(self.lower_bound, self.upper_bound + 1):
            if (1, i) in self.private_w:
                t_p = i
                s_w = self.private_w.pop((1, i))
                s_w.release()
                self.nbw_p[i] -= 1
                break

        new = {}
        for i in list(self.private_w.keys()):
            if i[1] == t_p:
                new[(i[0] - 1, t_p)] = self.private_w[(i[0], t_p)]
            else:
                new[i] = self.private_w[i]
        self.private_w = new

    def aging_priority(self):
        pass
