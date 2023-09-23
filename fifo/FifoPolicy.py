from fifo.FifoSem import FifoSem
from generals.Policy import Policy
import time
import random


class FifoPolicy(Policy):
    __s = FifoSem()

    def empty(self, i=-1):
        self.__s.before_reading(i)
        ris = self.nq.empty_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.__s.after_reading()
        return ris

    def get_head(self, i=-1):
        self.__s.before_reading(i)
        ris = self.nq.get_head_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.__s.after_reading()
        return ris

    def get_length(self, i=-1):
        self.__s.before_reading(i)
        ris = self.nq.get_length_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.__s.after_reading()
        return ris

    def pop(self, i=-1):
        self.__s.before_writing(i)
        ris = self.nq.pop_not_safe()
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.__s.after_writing()
        return ris

    def push(self, new_node, i=-1):
        self.__s.before_writing(i)
        self.nq.push_not_safe(new_node)
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.__s.after_writing()
