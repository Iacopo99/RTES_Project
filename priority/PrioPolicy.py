from generals.Policy import Policy
from priority.PrioSem import PrioSem
import random
import time


class PrioPolicy(Policy):
    sem = PrioSem()

    def __init__(self, head=None, lower_bound=0, upper_bound=4):
        super().__init__(head)
        self.sem = PrioSem(lower_bound, upper_bound)

    def empty(self, i):
        self.sem.before_reading(i)
        ris = self.nq.empty_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.sem.after_reading()
        return ris

    def get_head(self, i):
        self.sem.before_reading(i)
        ris = self.nq.get_head_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.sem.after_reading()
        return ris

    def get_length(self, i):
        self.sem.before_reading(i)
        ris = self.nq.get_length_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.sem.after_reading()
        return ris

    def pop(self, i, prio=sem.def_prio):
        self.sem.before_writing(i, prio)
        ris = self.nq.pop_not_safe()
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.sem.after_writing()
        return ris

    def push(self, i, new_node, prio=sem.def_prio):
        self.sem.before_writing(i, prio)
        self.nq.push_not_safe(new_node)
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.sem.after_writing()
