from generals.Policy import Policy
from priority.PrioSem import PrioSem
import random
import time


class PrioPolicy(Policy):
    sem = PrioSem()

    def __init__(self, head=None, lower_bound=0, upper_bound=4):
        """
        Create a queue of elements that multiple threads can modify in a thread-safe mode following the static priority policy.\n
        :param head: If specified insert the first element of the queue. Otherwise the queue created is empty.
        :param lower_bound: An int number containing the highest priority to assign (the lowest number)
        :param upper_bound: An int number containing the lowest priority to assign (the highest number)
        """
        super().__init__(head)
        self.sem = PrioSem(lower_bound, upper_bound)

    def __general_reader(self, func, i):
        self.sem.before_reading(i)
        ris = func()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.sem.after_reading()
        return ris

    def empty(self, i):
        return self.__general_reader(self.nq.empty_not_safe, i)

    def get_head(self, i):
        return self.__general_reader(self.nq.get_head_not_safe, i)

    def get_length(self, i):
        return self.__general_reader(self.nq.get_length_not_safe, i)

    def __general_writer(self, func, i, prio, new_node=None):
        self.sem.before_writing(i, prio)
        if new_node is None:
            ris = func()
        else:
            ris = func(new_node)
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.sem.after_writing()
        return ris

    def pop(self, i, prio=sem.def_prio):
        return self.__general_writer(self.nq.pop_not_safe, i, prio)

    def push(self, i, new_node, prio=sem.def_prio):
        self.__general_writer(self.nq.push_not_safe, i, prio, new_node)
