import random
from rr.RRSem import RRSem
from generals.Policy import Policy
import time


class RRPolicy(Policy):
    start = 0
    end = 0
    thread_time = {}

    def __init__(self, head=None, q=3):
        super().__init__(head)
        self.q = q
        self.s = RRSem(q)

    def empty(self, i=-1):
        return self.general_reading(self.nq.empty_not_safe, i)

    def get_head(self, i=-1):
        return self.general_reading(self.nq.get_head_not_safe, i)

    def get_length(self, i=-1):
        return self.general_reading(self.nq.get_length_not_safe, i)

    def general_reading(self, func, i):
        self.s.before(i)
        start = time.time()
        ris = func()
        time.sleep(float(random.randint(0, 300) / 1000))
        end = time.time()
        t = self.calculate_t(i, end - start)
        print('funz eseguita in {} secondi'.format(t))
        self.s.after(t, i)
        return ris

    def general_writing(self, func, i, node=None):
        self.s.before(i)
        start = time.time()
        if node is None:
            ris = func()
        else:
            ris = func(node)
        time.sleep(float(random.randint(0, 1000) / 1000))
        end = time.time()
        t = self.calculate_t(i, end - start)
        self.s.after(t, i)
        return ris

    def pop(self, i=-1):
        return self.general_writing(self.nq.pop_not_safe, i)

    def push(self, new_node, i=-1):
        self.general_writing(self.nq.push_not_safe, i, new_node)

    def calculate_t(self, i, t):
        if i in self.thread_time:
            if self.thread_time[i] >= self.q:
                self.thread_time[i] = 0
            self.thread_time[i] += t
        else:
            self.thread_time[i] = t
        return self.thread_time[i]
