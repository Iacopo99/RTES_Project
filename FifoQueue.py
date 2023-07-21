import random
import time

from NormalQueue import NormalQueue
from FifoSem import FifoSem


class FifoQueue:
    s = FifoSem()

    def __init__(self, head=None):
        """
        Create an FifoQueue object
        :param head: If specified insert the first element of the queue. Otherwise the queue created is empty.
        """
        self.nq = NormalQueue(head)

    def __str__(self):
        self.s.before_reading(None)
        ris = self.nq.str_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def empty(self, i=-1):
        """
        Returns a boolean variable. True if the queue is empty (no elements), False otherwise
        :param i: The index of thread that is running the function
        :return: Boolean variable
        """
        self.s.before_reading(i)
        ris = self.nq.empty_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def get_head(self, i=-1):
        """
        Returns the first object in the queue
        :param i: The index of thread that is running the function
        :return: Any possible type of object
        """
        self.s.before_reading(i)
        ris = self.nq.get_head_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def get_length(self, i=-1):
        """
        Returns the number of elements in the queue
        :param i: The index of thread that is running the function
        :return: An integer the represent the length
        """
        self.s.before_reading(i)
        ris = self.nq.get_length_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def pop(self, i=-1):
        """
        Select the first item in the queue and deletes the object from it
        :param i: The index of thread that is running the function
        :return: The first object of the queue
        """
        self.s.before_writing(i)
        ris = self.nq.pop_not_safe()
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.s.after_writing()
        return ris

    def push(self, new_node, i=-1):
        """
        Add an item at the end of the fifo Queue
        :param new_node: It is the item to add in the queue
        :param i: The index of thread that is running the function
        :return: Nothing
        """
        self.s.before_writing(i)
        self.nq.push_not_safe(new_node)
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.s.after_writing()
