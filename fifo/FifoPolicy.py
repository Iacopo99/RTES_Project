from fifo.FifoSem import FifoSem
from generals.Policy import Policy
import time
import random


class FifoPolicy(Policy):
    __s = FifoSem()

    def general_reader(self, func, i=-1):
        self.__s.before_reading(i)
        ris = func()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.__s.after_reading()
        return ris

    def empty(self, i=-1):
        return self.general_reader(self.nq.empty_not_safe, i)

    def get_head(self, i=-1):
        return self.general_reader(self.nq.get_head_not_safe, i)

    def get_length(self, i=-1):
        return self.general_reader(self.nq.get_length_not_safe, i)

    def general_writer(self, func, i=-1, node=None):
        self.__s.before_writing(i)
        if node is None:
            ris = func()
        else:
            ris = func(node)
        time.sleep(float(random.randint(0, 300) / 1000))
        self.__s.after_writing()
        return ris

    def pop(self, i=-1):
        return self.general_writer(self.nq.pop_not_safe, i)

    def push(self, new_node, i=-1):
        self.general_writer(self.nq.push_not_safe, i, new_node)
