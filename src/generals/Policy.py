from generals.ImplementSem import ImplementSem
import random
import time
from generals.NormalQueue import NormalQueue


class Policy:
    s = ImplementSem()

    def __init__(self, head=None):
        """
        Create a queue of elements that multiple threads can modify in a thread-safe mode following a specific policy.\n
        :param head: If specified insert the first element of the queue. Otherwise the queue created is empty.
        """
        self.nq = NormalQueue(head)

    def __str__(self):
        self.s.before_reading()
        ris = self.nq.str_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def empty(self, i):
        """
        Returns a boolean variable. True if the queue is empty (no elements), False otherwise
        :param i: the running thread id
        :return: Boolean variable
        """
        pass

    def get_head(self, i):
        """
        Returns the first object in the queue
        :param i: the running thread id
        :return: Any possible type of object
        """
        pass

    def get_length(self, i):
        """
        Returns the number of elements in the queue
        :param i: the running thread id
        :return: An integer the represent the length
        """
        pass

    def pop(self, i):
        """
        Select the first item in the queue and deletes the object from it
        :param i: the running thread id
        :return: The first object of the queue
        """
        pass

    def push(self, i, new_node):
        """
        Add an item at the end of the fifo Queue
        :param i: the running thread id
        :param new_node: It is the item to add in the queue
        :return: Nothing
        """
        pass
