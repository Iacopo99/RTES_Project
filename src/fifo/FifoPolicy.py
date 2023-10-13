from fifo.FifoSem import FifoSem
from generals.Policy import Policy
import time
import random


class FifoPolicy(Policy):
    sem = FifoSem()

    def __init__(self, head=None):
        """
        Create a queue of elements that multiple threads can modify in a thread-safe mode following the Fifo scheduling policy.\n
        :param head: If specified insert the first element of the queue. Otherwise the queue created is empty.
        """
        super().__init__(head)

    def __general_reader(self, func, i):
        self.sem.before_reading(i)
        ris = func()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.sem.after_reading()
        return ris

    def empty(self, i=-1):
        return self.__general_reader(self.nq.empty_not_safe, i)

    def get_head(self, i=-1):
        return self.__general_reader(self.nq.get_head_not_safe, i)

    def get_length(self, i=-1):
        return self.__general_reader(self.nq.get_length_not_safe, i)

    def __general_writer(self, func, i, node=None):
        self.sem.before_writing(i)
        if node is None:
            ris = func()
        else:
            ris = func(node)
        time.sleep(float(random.randint(0, 300) / 1000))
        self.sem.after_writing()
        return ris

    def pop(self, i=-1):
        return self.__general_writer(self.nq.pop_not_safe, i)

    def push(self, new_node, i=-1):
        self.__general_writer(self.nq.push_not_safe, i, new_node)
