from Generals.Policy import Policy
from PrioSem import PrioSem
import random
import time


class PrioPolicy(Policy):
    s = PrioSem()

    def empty(self, i=-1, prio=s.def_prio):
        self.s.before_reading(i)
        ris = self.nq.empty_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def get_head(self, i=-1, prio=s.def_prio):
        self.s.before_reading(i)
        ris = self.nq.get_head_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def get_length(self, i=-1, prio=s.def_prio):
        self.s.before_reading(i)
        ris = self.nq.get_length_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def pop(self, i=-1, prio=s.def_prio):
        self.s.before_writing(i, prio)
        ris = self.nq.pop_not_safe()
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.s.after_writing()
        return ris

    def push(self, new_node, i=-1, prio=s.def_prio):
        self.s.before_writing(i, prio)
        self.nq.push_not_safe(new_node)
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.s.after_writing()
