from Sem import Sem
from NormalQueue import NormalQueue


class FifoQueue:
    s = Sem()

    def __init__(self, head=None):
        self.nq = NormalQueue(head)

    def __str__(self, i):
        self.s.before_reading(i)
        ris = self.nq.str_not_safe()
        self.s.after_reading()
        return ris

    def empty(self, i):
        self.s.before_reading(i)
        ris = self.nq.empty_not_safe()
        self.s.after_reading()
        return ris

    def get_head(self, i):
        self.s.before_reading(i)
        ris = self.nq.get_head_not_safe()
        self.s.after_reading()
        return ris

    def get_length(self, i):
        self.s.before_reading(i)
        ris = self.nq.get_length_not_safe()
        self.s.after_reading()
        return ris

    def pop(self, i):
        self.s.before_writing(i)
        ris = self.nq.pop_not_safe()
        self.s.after_writing()
        return ris

    def push(self, new_node, i):
        self.s.before_writing(i)
        self.nq.push_not_safe(new_node)
        self.s.after_writing()

